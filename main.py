"""
yolo_live_gui_v6.py
-------------------
YOLO Live Detection GUI with:
✅ Start / Stop / Record buttons
✅ Confidence slider
✅ Detection counter + log panel
✅ Auto snapshot saving for gun/knife
✅ Preview of 3 most recent snapshots
✅ "Open Snapshot Folder" button
"""

import tkinter as tk
from tkinter import messagebox, ttk
from PIL import Image, ImageTk
import cv2
import threading
import time
from ultralytics import YOLO
from datetime import datetime
import os
import subprocess
import platform

# ---------------------------
# Configuration
# ---------------------------
MODEL_PATH = r"C:/Users/Qc/Desktop/P/runs/detect/train3/weights/best.pt"  # Your trained YOLO model
DEVICE = "cpu"
IMG_SIZE = 320
ALERT_CLASSES = {"gun", "knife"}
SNAPSHOT_DIR = "detections"

os.makedirs(SNAPSHOT_DIR, exist_ok=True)


# ---------------------------
# Helper Functions
# ---------------------------
def draw_boxes(frame, results, min_conf=0.3):
    """Draw bounding boxes and return detected class names."""
    boxes = results[0].boxes
    names = results[0].names
    detections = []

    if boxes is not None and len(boxes) > 0:
        for xyxy, conf, cls in zip(boxes.xyxy, boxes.conf, boxes.cls):
            if conf < min_conf:
                continue
            x1, y1, x2, y2 = map(int, xyxy)
            cls_id = int(cls)
            label = f"{names[cls_id]} {conf:.2f}"
            detections.append(names[cls_id])
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
            cv2.putText(frame, label, (x1, max(y1 - 10, 10)),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
    return frame, detections


def save_snapshot(frame, obj_name):
    """Save a snapshot image when specific object detected."""
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    filename = f"{SNAPSHOT_DIR}/{obj_name}_{timestamp}.jpg"
    cv2.imwrite(filename, frame)
    return filename


def open_folder(path):
    """Open a folder cross-platform."""
    if platform.system() == "Windows":
        os.startfile(os.path.realpath(path))
    elif platform.system() == "Darwin":
        subprocess.Popen(["open", os.path.realpath(path)])
    else:
        subprocess.Popen(["xdg-open", os.path.realpath(path)])


# ---------------------------
# GUI Application
# ---------------------------
class YOLOGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("YOLO Live Detection GUI v6")
        self.root.geometry("1220x650")
        self.root.resizable(False, False)

        # Model
        self.model = YOLO(MODEL_PATH)
        self.model.to(DEVICE)

        # Flags
        self.cap = None
        self.running = False
        self.recording = False
        self.out = None
        self.total_detections = 0
        self.conf_threshold = tk.DoubleVar(value=0.5)
        self.recent_snapshots = []

        # ===============================
        # Layout
        # ===============================
        main_frame = tk.Frame(root, bg="#202020")
        main_frame.pack(fill="both", expand=True)

        self.label = tk.Label(main_frame, bg="black")
        self.label.place(x=20, y=20, width=640, height=480)

        # Buttons
        btn_frame = tk.Frame(main_frame, bg="#202020")
        btn_frame.place(x=680, y=20)

        self.start_btn = tk.Button(btn_frame, text="Start", bg="#4CAF50", fg="white",
                                   font=("Arial", 12, "bold"), width=10, command=self.start_detection)
        self.start_btn.grid(row=0, column=0, padx=5, pady=5)

        self.stop_btn = tk.Button(btn_frame, text="Stop", bg="#f44336", fg="white",
                                  font=("Arial", 12, "bold"), width=10, command=self.stop_detection)
        self.stop_btn.grid(row=0, column=1, padx=5, pady=5)

        self.record_btn = tk.Button(btn_frame, text="Record", bg="#FF9800", fg="white",
                                    font=("Arial", 12, "bold"), width=10, command=self.toggle_record)
        self.record_btn.grid(row=1, column=0, columnspan=2, pady=5)

        # Confidence slider
        slider_frame = tk.LabelFrame(main_frame, text="Confidence Threshold",
                                     bg="#202020", fg="white", font=("Arial", 10, "bold"))
        slider_frame.place(x=680, y=120, width=240, height=100)
        self.conf_slider = ttk.Scale(slider_frame, from_=0.1, to=1.0,
                                     orient="horizontal", variable=self.conf_threshold)
        self.conf_slider.pack(padx=10, pady=10, fill="x")
        self.conf_value_label = tk.Label(slider_frame, text="0.50", fg="white",
                                         bg="#202020", font=("Arial", 10))
        self.conf_value_label.pack()
        self.conf_threshold.trace("w", self.update_conf_label)

        # Detection log
        log_frame = tk.LabelFrame(main_frame, text="Detection Log",
                                  bg="#202020", fg="white", font=("Arial", 10, "bold"))
        log_frame.place(x=680, y=240, width=240, height=260)
        self.detection_count_label = tk.Label(log_frame, text="Total Detections: 0",
                                              fg="yellow", bg="#202020", font=("Arial", 11, "bold"))
        self.detection_count_label.pack(pady=5)
        self.log_box = tk.Text(log_frame, width=28, height=12, bg="#111",
                               fg="#00FF00", font=("Consolas", 9))
        self.log_box.pack(padx=5, pady=5)
        self.log_box.insert(tk.END, "Detection logs will appear here...\n")

        # Snapshot preview
        preview_frame = tk.LabelFrame(main_frame, text="Recent Snapshots",
                                      bg="#202020", fg="white", font=("Arial", 10, "bold"))
        preview_frame.place(x=940, y=20, width=260, height=480)
        self.preview_labels = []
        for i in range(3):
            lbl = tk.Label(preview_frame, bg="black")
            lbl.pack(padx=5, pady=5)
            self.preview_labels.append(lbl)

        # Open Folder button
        self.open_folder_btn = tk.Button(main_frame, text="Open Snapshot Folder",
                                         bg="#2196F3", fg="white", font=("Arial", 11, "bold"),
                                         width=25, command=lambda: open_folder(SNAPSHOT_DIR))
        self.open_folder_btn.place(x=940, y=520)

        self.status_label = tk.Label(main_frame, text="Status: Idle",
                                     font=("Arial", 11), fg="white", bg="#202020")
        self.status_label.place(x=20, y=520)

    # -----------------------
    # Button Handlers
    # -----------------------
    def start_detection(self):
        if not self.running:
            self.running = True
            self.cap = cv2.VideoCapture(0)
            if not self.cap.isOpened():
                messagebox.showerror("Error", "Cannot open camera")
                self.running = False
                return
            self.status_label.config(text="Status: Running")
            threading.Thread(target=self.detect_loop, daemon=True).start()

    def stop_detection(self):
        self.running = False
        self.status_label.config(text="Status: Stopped")
        if self.cap:
            self.cap.release()
        if self.out:
            self.out.release()
            self.out = None

    def toggle_record(self):
        if not self.running:
            messagebox.showinfo("Info", "Start detection before recording.")
            return
        self.recording = not self.recording
        if self.recording:
            fourcc = cv2.VideoWriter_fourcc(*'mp4v')
            self.out = cv2.VideoWriter("output.mp4", fourcc, 20.0, (640, 480))
            self.record_btn.config(bg="#E91E63", text="Recording...")
            self.status_label.config(text="Status: Recording")
        else:
            if self.out:
                self.out.release()
                self.out = None
            self.record_btn.config(bg="#FF9800", text="Record")
            self.status_label.config(text="Status: Running")

    def update_conf_label(self, *args):
        self.conf_value_label.config(text=f"{self.conf_threshold.get():.2f}")

    # -----------------------
    # Detection Loop
    # -----------------------
    def detect_loop(self):
        prev_time = 0
        while self.running:
            ret, frame = self.cap.read()
            if not ret:
                break

            conf_val = float(self.conf_threshold.get())
            results = self.model.predict(frame, imgsz=IMG_SIZE, device=DEVICE, verbose=False)
            frame, detections = draw_boxes(frame, results, min_conf=conf_val)

            if detections:
                self.total_detections += len(detections)
                self.detection_count_label.config(text=f"Total Detections: {self.total_detections}")
                timestamp = datetime.now().strftime("%H:%M:%S")

                for obj in detections:
                    self.log_box.insert(tk.END, f"[{timestamp}] {obj}\n")
                    self.log_box.see(tk.END)

                    if obj.lower() in ALERT_CLASSES:
                        snapshot_path = save_snapshot(frame, obj.lower())
                        self.update_preview(snapshot_path)

            # FPS
            curr_time = time.time()
            fps = 1 / (curr_time - prev_time) if prev_time else 0
            prev_time = curr_time
            cv2.putText(frame, f"FPS: {fps:.1f}", (10, 25),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 2)

            if self.recording and self.out:
                self.out.write(frame)

            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            img = Image.fromarray(frame_rgb)
            imgtk = ImageTk.PhotoImage(image=img)
            self.label.imgtk = imgtk
            self.label.configure(image=imgtk)

            self.root.update_idletasks()
            self.root.update()

        self.stop_detection()

    def update_preview(self, new_image_path):
        """Update the recent snapshot thumbnails."""
        self.recent_snapshots.insert(0, new_image_path)
        self.recent_snapshots = self.recent_snapshots[:3]  # Keep 3 latest

        for i, lbl in enumerate(self.preview_labels):
            if i < len(self.recent_snapshots):
                img = Image.open(self.recent_snapshots[i])
                img.thumbnail((220, 120))
                imgtk = ImageTk.PhotoImage(img)
                lbl.imgtk = imgtk
                lbl.configure(image=imgtk)
            else:
                lbl.configure(image="", bg="black")

    def on_close(self):
        self.running = False
        if self.cap:
            self.cap.release()
        if self.out:
            self.out.release()
        self.root.destroy()


# ---------------------------
# Run
# ---------------------------
if __name__ == "__main__":
    root = tk.Tk()
    app = YOLOGUI(root)
    root.protocol("WM_DELETE_WINDOW", app.on_close)
    root.mainloop()
