import cv2
import numpy as np

image = np.ones((512, 512, 3), dtype=np.uint8) * 255

center = (256, 256)

cv2.ellipse(image, (center[0] - 50, center[1] - 50), (60, 100), 0, 0, 360, (255, 0, 0), -1)

cv2.ellipse(image, (center[0] + 50, center[1] - 50), (60, 100), 120, 0, 360, (0, 255, 0), -1)

cv2.ellipse(image, (center[0], center[1] + 60), (60, 100), 240, 0, 360, (0, 0, 255), -1)

cv2.putText(image, 'OpenCV', (170, 460), cv2.FONT_HERSHEY_SIMPLEX, 1.8, (0, 0, 0), 4)

cv2.imwrite("opencv_logo.jpg", image)
