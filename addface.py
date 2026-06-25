import cv2
import os

# 1. Ensure folder exists
os.makedirs("known_faces", exist_ok=True)

# 2. Ask for the user's name in the terminal first
name = input("Enter the name of the person being enrolled: ").strip()
if not name:
    print("Name cannot be empty!")
    exit()

filename = f"known_faces/{name}.jpg"

# 3. Start the camera
camera = cv2.VideoCapture(0)
print(f"📸 Look at the camera and press SPACEBAR to enroll {name}.")

while True:
    ret, frame = camera.read()
    if not ret: break

    # Visual overlay instructions
    cv2.putText(frame, f"Enrolling: {name}", (50, 50), cv2.FONT_HERSHEY_DUPLEX, 1, (0, 255, 0), 2)
    cv2.putText(frame, "Press SPACE to capture", (50, 90), cv2.FONT_HERSHEY_DUPLEX, 0.7, (255, 255, 255), 1)
    
    cv2.imshow("Security Setup - Enrollment", frame)
    key = cv2.waitKey(1)
    
    # Spacebar captures and saves
    if key % 256 == 32: 
        cv2.imwrite(filename, frame)
        print(f"Photo saved successfully")
        break
    elif key & 0xFF == ord('q'):
        print("Enrollment cancelled.")
        break

camera.release()
cv2.destroyAllWindows()