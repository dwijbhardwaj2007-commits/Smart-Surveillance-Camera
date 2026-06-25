import cv2
import numpy as np
import os

# 1. Initialize face utilities
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
recognizer = cv2.face.LBPHFaceRecognizer_create()

# Dynamic registry arrays
face_samples = []
face_ids = []
name_registry = {}  # Maps number IDs back to text names (e.g., {1: "Dwij", 2: "Mom"})

print("Scanning database and viewing registered faces")

folder_path = "known_faces"
if not os.path.exists(folder_path) or len(os.listdir(folder_path)) == 0:
    print("Error: No faces found!")
    exit()

current_id = 1

# 2. Dynamic Training Loop
for filename in os.listdir(folder_path):
    if filename.endswith(".jpg") or filename.endswith(".jpeg") or filename.endswith(".png"):
        # Extract the person's name from the image filename
        person_name = os.path.splitext(filename)[0]
        image_path = os.path.join(folder_path, filename)
        
        # Load profile in grayscale
        img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
        faces_in_photo = face_cascade.detectMultiScale(img, scaleFactor=1.1, minNeighbors=5)
        
        for (x, y, w, h) in faces_in_photo:
            face_samples.append(img[y:y+h, x:x+w])
            face_ids.append(current_id)
            
        # Map this specific ID to the person's name
        name_registry[current_id] = person_name
        print(f"   [Indexed] ID {current_id}: {person_name}")
        current_id += 1

# Train the recognizer with all gathered data arrays
if len(face_samples) > 0:
    recognizer.train(face_samples, np.array(face_ids))
    print("Starting Face Recognition")
else:
    print("Error: Could not detect clear face data in your saved photos to train the AI.")
    exit()

# 3. Live Video Stream Pipeline
camera = cv2.VideoCapture(0)

while True:
    ret, frame = camera.read()
    if not ret: break

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    live_faces = face_cascade.detectMultiScale(gray, scaleFactor=1.2, minNeighbors=5)

    for (x, y, w, h) in live_faces:
        live_face_crop = gray[y:y+h, x:x+w]
        
        # Predict returns the ID number and a math difference confidence score
        id_prediction, distance = recognizer.predict(live_face_crop)

        # Stricter verification threshold (lower = tighter)
        if distance < 43:  
            name = name_registry.get(id_prediction, "Unknown User")
            color = (0, 255, 0)  # Green for verified profiles
        else:
            name = "Unknown Intruder"
            color = (0, 0, 255)  # Red for unrecognized individuals

        # 4. Draw bounding annotations
        cv2.rectangle(frame, (x, y), (x+w, y+h), color, 2)
        cv2.putText(frame, name, (x, y-10), cv2.FONT_HERSHEY_DUPLEX, 0.8, color, 1)
        
        # Calibration Metrics Overlay
        cv2.putText(frame, f"Dist: {int(distance)} (ID: {id_prediction})", (x, y+h+25), 
                    cv2.FONT_HERSHEY_DUPLEX, 0.6, (255, 255, 255), 1)

    cv2.imshow('Identity Verification Engine', frame)

    # Press 'c' to safely exit the feed loop
    if cv2.waitKey(1) & 0xFF == ord('c'):
        break

camera.release()
cv2.destroyAllWindows()