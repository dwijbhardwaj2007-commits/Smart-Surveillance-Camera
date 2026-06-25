content = """# Smart Security Camera MVP

## Overview
A real-time, local edge-inference security camera prototype built with Python. This MVP features YOLOv8-based threat detection (weapons) and dlib-based facial recognition to distinguish between authorized users and unknown intruders. Designed to run completely on-device for maximum privacy and zero cloud latency.

## Features
* **Live Video Processing:** High-FPS webcam feed integration using OpenCV.
* **Threat Detection (`camera.py`):** Uses a custom YOLOv8 model (`best.pt`) to detect weapons (pistols, knives, etc.) with a configurable confidence threshold.
* **Identity Verification (`identity.py`):** Uses the `face_recognition` library to match live faces against a secure local database of known users, flagging unrecognized faces as "Unknown Intruder."
* **Edge Inference:** 100% local processing; no internet connection required after setup.

## Prerequisites
* macOS (Apple Silicon or Intel)
* Python 3.8+
* A built-in or USB webcam

## Installation & Setup

1. **Set up Virtual Environment**
   Code output
   README.md generated successfully.
   
   python3 -m venv venv
   source venv/bin/activate
2. Install Core Dependencies
pip install opencv-python ultralytics cmake face_recognition
(Note: cmake is required before installing face_recognition as it compiles C++ binaries).
3. Configure the Threat Engine
Place your custom YOLOv8 weights file (named best.pt) directly into the root project folder.
4. Configure the Identity Engine
Create a folder named known_faces/ in the project root.
Add a clear, front-facing .jpg image of yourself (e.g., Dwij.jpg).
5. Usage
Activate the environment first:
source venv/bin/activate
6. Run Threat Detection (Weapons/Masks):
python3 camera.py
Press c to close the window.
7. Run Identity Verification:
python3 identity.py
Press q to close the window.
