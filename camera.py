import cv2
from ultralytics import YOLO
# 1. Access the MacBook camera
camera = cv2.VideoCapture(0)
model = YOLO('best.pt')
while True:
    # 2. Grab each frame from the camera
    ret, frame = camera.read()  
    if not ret:
        break
    results = model(frame)
    # 3. Show the video feed in a window
    annotated_frame = results[0].plot()
    cv2.imshow("Smart Detection Camera", annotated_frame)  
    # 4. Stop the loop if you press the 'c' key
    if cv2.waitKey(1) & 0xFF == ord('c'):
        break
# 5. Turn off the camera when done
camera.release()
cv2.destroyAllWindows()

