# Motoplat

## 🚀 License Plate Detection, Recognition, and Moving Motorcycle Identification System 
### Using YOLOv10 and EasyOCR

This repository contains the source code for my undergraduate thesis project, focused on detecting motorcycles and recognizing license plates from video input using deep learning.

## 📚 Project Overview

This project aims to build an intelligent system that can:
- Detect motorcycles and license plates in traffic videos
- Extract and recognize license plate characters using OCR
- Provide text-based outputs for further processing or database integration

The system combines **YOLOv10** (for object detection) with **EasyOCR** (for license plate text recognition), and is implemented in **Python** using **OpenCV** and **PyTorch** frameworks.

## 🎯 Objectives
- Detect moving motorcycles and their license plates in real-time.
- Recognize license plate text automatically and accurately.
- Learn and apply deep learning methods in a real-world scenario.

## 🧠 Technologies Used
| Component          | Technology / Library     |
|-------------------|--------------------------|
| Object Detection  | YOLOv10 (Ultralytics-based) |
| OCR               | EasyOCR                  |
| Image Processing  | OpenCV                   |
| Programming Language | Python                |
| Deep Learning Framework | PyTorch            |


## 🛠️ Installation

1. Clone this repository:
```bash
git clone https://github.com/Erastus12/Motoplat.git
cd Motoplat
```

2. Create a virtual environment and install dependencies:
```bash
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install -r requirements.txt
```

3. Import database and run MySQL server

4. Download YOLOv10 pretrained weights and place them in the models/ folder.
```bash
python src/detection.py --input input/contoh_3.mp4
```

The script will:

Detect motorcycles and license plates

Run OCR on the detected plates

Output results to the output/ folder

✅ Sample Output
🎥 Video with bounding boxes and detected plates

📸 Cropped images of detected plates

📝 Text files with recognized license numbers


🙋‍♂️Author
Erastus Keytaro Bangun - Information Technology Graduate, Universitas Sumatera Utara



