🔫 Weapon Detection System (YOLO Live GUI v6)

A real-time AI-powered weapon detection system built using YOLOv8, OpenCV, and Tkinter GUI.
This system can detect guns and knives from a live camera feed, displaying bounding boxes and confidence scores, automatically saving snapshots, and providing an intuitive interface for real-time monitoring and recording.

🚀 Features

🎥 Real-time detection using YOLOv8 (CPU-compatible)

⚙️ Detects guns and knives with high accuracy

🖥️ Modern GUI with Start / Stop / Record buttons

🎚️ Adjustable confidence threshold slider

📈 Real-time detection log and counter

📸 Auto snapshot saving on detection

🖼️ Preview panel for latest snapshots

📁 Open Snapshot Folder button

💾 Optional recording of live video

🛠️ Tech Stack

Python 3.x

YOLOv8 (Ultralytics)

OpenCV

Tkinter

Pillow (PIL)

📂 Project Structure
├── best.pt                 # Trained YOLO model
├── yolo_live_gui_v6.py     # Main application
├── detections/             # Auto-saved snapshots
├── dataset/                # Custom dataset (optional)
│   ├── data.yaml
│   ├── train/
│   └── val/
└── output.mp4              # Optional recorded video

⚙️ How to Run

Clone the repository

git clone https://github.com/yourusername/Weapon-Detection-GUI.git
cd Weapon-Detection-GUI
Install dependencies

pip install ultralytics opencv-python pillow

Run the GUI

python yolo_live_gui_v6.py


Use the interface to start detection, record video, or review snapshots.

🧩 Model Training (Optional)

If you want to train or fine-tune your own YOLO model on a custom dataset:

1️⃣ Prepare Your Dataset

Organize your dataset folder as follows:

dataset/
├── images/
│   ├── train/
│   └── val/
├── labels/
│   ├── train/
│   └── val/
└── data.yaml

2️⃣ Example data.yaml
train: ./dataset/images/train
val: ./dataset/images/val

nc: 2
names: ['gun', 'knife']

3️⃣ Train Your Model
from ultralytics import YOLO

model = YOLO('yolov8n.pt')  # or yolov8s.pt for better accuracy
model.train(
    data='dataset/data.yaml',
    epochs=15,
    imgsz=640,
    batch=32,
    lr0=0.01,
    lrf=0.001,
    augment=True,
    mosaic=1.0,
    mixup=0.15,
    device='cpu'  # change to 'cuda' if GPU available
)

4️⃣ Save & Replace Model

After training, replace your best.pt file in the project folder with your newly trained weights.

🎯 Future Enhancements

☁️ Cloud-based alert and logging system

📡 Multi-camera input support

🧠 Improved model accuracy with additional classes

🔔 Integration with IoT or security platforms

📸 Preview
<img width="483" height="566" alt="Screenshot 2025-10-29 001111" src="https://github.com/user-attachments/assets/81924156-8fd9-4840-a095-a8d3f75f897c" />
<img width="1536" height="1024" alt="YOLO Knife Detection Interface" src="https://github.com/user-attachments/assets/61567217-c1da-4b2a-9c55-fda3d36b28a2" />
![val_batch1_pred](https://github.com/user-attachments/assets/a88718df-908a-46a1-b551-697bcd030d4a)
![val_batch0_labels](https://github.com/user-attachments/assets/137ccd76-f66a-40b8-b4c1-466a84c67cc8)
![train_batch2](https://github.com/user-attachments/assets/9fdf61fa-f201-4a87-99cc-458fea9c17d4)


🧠 About

This project showcases how AI and Computer Vision can be used to create intelligent, real-time safety systems capable of identifying potential threats and aiding in public security.
