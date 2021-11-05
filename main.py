import cv2 
import numpy as np 
import math
from cv2 import aruco

# Create a VideoCapture object and read from input file
# If the input is the camera, pass 0 instead of the video file name
cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
RED = [255,0,0]
aruco_dict = aruco.Dictionary_get(aruco.DICT_4X4_50)
parameters = aruco.DetectorParameters_create()

# Check if camera opened successfully
if (cap.isOpened()== False): 
  print("Error opening video stream or file")

# 640
frame_width = int(cap.get(3))
# 480
frame_height = int(cap.get(4))

out = cv2.VideoWriter('outpy.avi',cv2.VideoWriter_fourcc('M','J','P','G'), 10, (frame_width,frame_height))

# Read until video is completed
while(cap.isOpened()):
  # Capture frame-by-frame
  ret, frame = cap.read()
  if ret == True:  
    #draw lines

    cv2.line(img=frame, pt1=(0, 0), pt2=(0, 640), color=(255, 0, 0), thickness=2, lineType=32, shift=0)
    cv2.line(img=frame, pt1=(0, 0), pt2=(640, 0), color=(255, 0, 0), thickness=2, lineType=32, shift=0)
    cv2.line(img=frame, pt1=(640, 480), pt2=(0, 480), color=(255, 0, 0), thickness=2, lineType=32, shift=0)
    cv2.line(img=frame, pt1=(640, 480), pt2=(640, 0), color=(255, 0, 0), thickness=2, lineType=32, shift=0)

    cv2.line(img=frame, pt1=(0, 160), pt2=(640, 160), color=(255, 0, 0), thickness=2, lineType=8, shift=0)
    cv2.line(img=frame, pt1=(0, 320), pt2=(640, 320), color=(255, 0, 0), thickness=2, lineType=8, shift=0)
    cv2.line(img=frame, pt1=(0, 480), pt2=(640, 480), color=(255, 0, 0), thickness=2, lineType=8, shift=0)

    cv2.line(img=frame, pt1=(213, 0), pt2=(213, 480), color=(255, 0, 0), thickness=2, lineType=8, shift=0)
    cv2.line(img=frame, pt1=(416, 0), pt2=(416, 480), color=(255, 0, 0), thickness=2, lineType=8, shift=0)
    cv2.line(img=frame, pt1=(640, 0), pt2=(640, 480), color=(255, 0, 0), thickness=2, lineType=8, shift=0)

     # Edge detection
    dst = cv2.Canny(frame, 50, 200, None, 3)
    lines = cv2.HoughLines(dst, 1, np.pi / 180, 150, None, 0, 0)

    # Copy edges to the images that will display the results in BGR
    cdst = cv2.cvtColor(dst, cv2.COLOR_GRAY2BGR)
    cdstP = np.copy(cdst)
   
     # Draw the lines
    if lines is not None:
        for i in range(0, len(lines)):
            rho = lines[i][0][0]
            theta = lines[i][0][1]
            a = math.cos(theta)
            b = math.sin(theta)
            x0 = a * rho
            y0 = b * rho
            pt1 = (int(x0 + 1000*(-b)), int(y0 + 1000*(a)))
            pt2 = (int(x0 - 1000*(-b)), int(y0 - 1000*(a)))
            cv2.line(cdst, pt1, pt2, (0,0,255), 3, cv2.LINE_AA)

    # Probabilistic Line Transform
    linesP = cv2.HoughLinesP(dst, 1, np.pi / 180, 50, None, 50, 10)

     # Draw the lines
    if linesP is not None:
        for i in range(0, len(linesP)):
            l = linesP[i][0]
            cv2.line(cdstP, (l[0], l[1]), (l[2], l[3]), (0,0,255), 3, cv2.LINE_AA)

   # HARRIS CORNERS !
    # kernel= np.ones((7,7), np.uint8)
    # gray= cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    # harris_corners= cv2.cornerHarris(gray, 3, 3, 0.05)
    # harris_corners= cv2.dilate(harris_corners, kernel, iterations= 2)
    # frame[harris_corners > 0.025 * harris_corners.max()]= [255,127,127]

    #Write the frame into the file output
    #out.write(frame)

    # Detect the markers.
    corners, ids, rejectedImgPoints = aruco.detectMarkers(frame,aruco_dict,parameters=parameters)
    out = aruco.drawDetectedMarkers(frame, corners, ids)
    cv2.imshow("out",out)

    # Display the resulting frame
    cv2.imshow('Frame',frame)
    cv2.imshow('Detected Lines (in red) - Standard Hough Line Transform',cdst)
    cv2.imshow('Detected Lines (in red) - Probabilistic Line Transform',cdstP)

    # Press Q on keyboard to  exit
    if cv2.waitKey(25) & 0xFF == ord('q'):
      break

  # Break the loop
  else: 
    break

# When everything done, release the video capture object
cap.release()

# Closes all the frames
cv2.destroyAllWindows()
