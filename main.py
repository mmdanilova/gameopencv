import cv2
cap = cv2.VideoCapture(1)
while True:
    ret, frame = cap.read()
    if cv2.waitKey(1) & 0xFF == ord('q') or not ret:
        break
    cv2.imshow("Hands", frame)