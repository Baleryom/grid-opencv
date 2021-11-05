# GET IMAGE WEBCAM

import cv2 

cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)

return_value, image = cap.read()
cv2.imwrite("image.png", image)

cap.release()
