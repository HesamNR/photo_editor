import cv2
import numpy as np

img1 = cv2.imread("cat.jpg")
img2 = cv2.imread("cat(1).jpg")

img2 = cv2.resize(img2, (img1.shape[1], img1.shape[0]))

alpha = 0.5
blended = ((1 - alpha) * img1 + alpha * img2).astype(np.uint8)

cv2.imwrite("manual_blend.jpg", blended)
