import cv2
from ultralytics import YOLO

# 1. Load the YOLOv8 model
print("Loading YOLO model...")
model = YOLO('yolov8n.pt') 

# 2. Open the video feed (0 default webcam)
cap = cv2.VideoCapture(0)

print("Starting vision loop. Press 'q' to quit.")

while cap.isOpened():
    success, frame = cap.read()
    if not success:
        break

    # Get frame dimensions 
    frame_height, frame_width = frame.shape[:2]
    frame_center_x = int(frame_width / 2)
    frame_center_y = int(frame_height / 2)

    # 3. Run YOLOv8 inference on the frame
    results = model(frame, classes=0, verbose=False)

    for result in results:
        boxes = result.boxes
        for box in boxes:
            # 4. Extract bounding box coordinates
            x1, y1, x2, y2 = box.xyxy[0].int().tolist()

            # 5. Calculate the center of the bounding box
            target_center_x = int((x1 + x2) / 2)
            target_center_y = int((y1 + y2) / 2)

            # Draw the bounding box and the center dot
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
            cv2.circle(frame, (target_center_x, target_center_y), 5, (0, 0, 255), -1)

            # Draw a line from the center of the screen to the target
            cv2.line(frame, (frame_center_x, frame_center_y), (target_center_x, target_center_y), (255, 0, 0), 2)

    # Show the frame center as a green dot
    cv2.circle(frame, (frame_center_x, frame_center_y), 5, (0, 255, 0), -1)

    # Display the result
    cv2.imshow("YOLOv8 Target Tracking", frame)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()