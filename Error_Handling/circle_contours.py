import cv2 as cv
import numpy as np
import utils
from pyzbar import pyzbar



img = cv.imread("Photos/small_image.jpg")

contoursImage = img.copy()
grayImage = cv.cvtColor(img, cv.COLOR_RGB2BGR)  # gray image
blankImage = np.zeros_like(img)  # blank image
imgBigContour = img.copy()
imgContours = img.copy()
blurImage = cv.GaussianBlur(grayImage, (5, 5), 1)
cannyImage = cv.Canny(blurImage, 10, 70) # edge detection
threshImage = cv.threshold(grayImage, 140, 255, cv.THRESH_BINARY_INV)[1]

contours, hierarchy = cv.findContours(cannyImage, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_NONE)  # FIND ALL CONTOURS
cv.drawContours(imgContours, contours, -1, (0, 255, 0), -1) # here -1 means draw all contours
count_area = 0
for i,c in enumerate(contours):
    print(cv.contourArea(c))
    if cv.contourArea(c) < 20.0:
        count_area += 1

print(count_area)
# contous that are not circles: 101,113..117,118
# useless contours: 76,44,101,113,114,115,116,117,118 , need to find two more
# works fine: 11,22,33,making error(44),45,56,67,
# cv.imshow("Orginal Image", img)
# cv.imshow("Orginal Image", img)
imageArray = [img,blurImage,threshImage,imgContours]
allImages = utils.stackImages(imageArray, 1)
cv.imshow("All images", allImages)
# cv.imshow("contours",imgContours[2])# shows nothing google
print("total contours", len(contours))
print(img.shape)
print(blurImage.shape)
cv.waitKey(0)