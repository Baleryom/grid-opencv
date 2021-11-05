import numpy as np 
import cv2
from matplotlib import pyplot as plt


BLUE = [255,0,0]
img = cv2.imread('image.png')
h, w = img.shape[:2]

constant= cv2.copyMakeBorder(img,10,10,10,10,cv2.BORDER_CONSTANT,value=BLUE)
plt.subplot(236),plt.imshow(constant,'gray'),plt.title('CONSTANT')
plt.show()

x = np.arange(w)
polynomial1 = lambda x: x**2/800
polynomial2 = lambda x: x+200
y1 = polynomial1(x)
y2 = polynomial2(x)

points1 = np.array([[[xi, yi]] for xi, yi in zip(x, y1) if (0<=xi<w and 0<=yi<h)]).astype(np.int32)
points2 = np.array([[[xi, yi]] for xi, yi in zip(x, y2) if (0<=xi<w and 0<=yi<h)]).astype(np.int32)
points2 = np.flipud(points2)
points = np.concatenate((points1, points2))

polynomialgon = img.copy()
cv2.fillPoly(polynomialgon, [points], color=[255,255,255])
cv2.imshow('Polygon defined by two polynomials', polynomialgon)
cv2.waitKey(0)
