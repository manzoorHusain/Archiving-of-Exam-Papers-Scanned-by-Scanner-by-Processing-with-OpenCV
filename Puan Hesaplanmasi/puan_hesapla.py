import cv2 as cv
import numpy as np
import utlis
# img_path = "Photos/not_kutu1.png"
# img_path = "Photos/not_kutu2.png"
# img_path = "Photos/Cropped/crop_not_kutu2.png"
img_path = "Photos/Cropped/crop_not_kutu1_copy.png"
#image types
img = cv.imread(img_path)
grayImage = cv.cvtColor(img, cv.COLOR_RGB2BGR)# gray image
blankImage = np.zeros_like(img) # blank image
imgBigContour = img.copy()
contoursImage = img.copy()
# imgContours = img.copy()
blurImage = cv.GaussianBlur(grayImage,(5, 5), 1)
cannyImage = cv.Canny(blurImage,10,70)
threshImage  =  cv.threshold(grayImage, 150,255,cv.THRESH_BINARY_INV)[1]

# contours
contours, hierarchy = cv.findContours(cannyImage, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_NONE) # FIND ALL CONTOURS
cv.drawContours(contoursImage, contours, -1, (0, 255, 0), 1) 
# Displaying images 
imageArray = [[img,grayImage,blurImage],[cannyImage,threshImage,contoursImage]]
allImages = utlis.stackImages(imageArray,1)
cv.imshow("All Images",allImages)
# cv.imshow("Not kutu1",img)



cv.waitKey(0)