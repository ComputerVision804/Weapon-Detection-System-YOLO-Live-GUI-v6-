# Weapon-Detection-System-YOLO-Live-GUI-v6-
I’m thrilled to share my latest innovation  a real-time Weapon Detection System powered by Artificial Intelligence and Computer Vision.
This application detects guns and knives through a live camera feed and provides instant visual alerts, snapshot saving, and a user-friendly interface for live monitoring and recording.

🚀 Features

🎥 Live Detection using YOLOv8 (supports CPU)

🧠 Detects guns and knives with bounding boxes and confidence scores

🖥️ Interactive GUI with Start / Stop / Record buttons

🎚️ Confidence slider to adjust detection sensitivity

🧾 Real-time detection log and counter

📸 Automatic snapshot saving on weapon detection

🖼️ Preview panel for 3 recent snapshots

📁 “Open Snapshot Folder” button for quick access

💾 Optional recording mode (saves live detection video)
🛠️ Tech Stack
Python 3.x
YOLOv8 (Ultralytics)
OpenCV
Tkinter
Pillow (PIL)

📂 Project Structure
├── best.pt                 # Trained YOLO model
├── yolo_live_gui_v6.py     # Main application
├── detections/             # Saved snapshots
└── output.mp4              # Optional recorded video

⚙️ How to Run

Clone the repository

git clone https://github.com/yourusername/Weapon-Detection-GUI.git
cd Weapon-Detection-GUI


Install dependencies

pip install ultralytics opencv-python pillow

Run the application

python yolo_live_gui_v6.py

Use the GUI to start/stop detection, record video, and view snapshots.

🎯 Future Enhancements

🔔 Real-time cloud or email alerts

🌐 Multi-camera support

🧩 Integration with security systems or APIs

☁️ Cloud-based logging and dashboard

📸 Preview

<img width="1536" height="1024" alt="YOLO Knife Detection Interface" src="https://github.com/user-attachments/assets/0921eedb-d9bc-4138-aaac-778e3c44b5e2" />



🧠 About

This project demonstrates how AI and computer vision can enhance public safety through intelligent, real-time monitoring and weapon detection.
