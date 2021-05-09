import cv2 as cv
import numpy as np
import utlis
widthImg = 300
heightImg = 300
questions = 11
img = cv.imread('Photos/new_image.jpg')
img = cv.resize(img, (widthImg, heightImg))
contoursImage = img.copy()
grayImage = cv.cvtColor(img, cv.COLOR_RGB2BGR)# gray image
blankImage = np.zeros_like(img) # blank image
imgBigContour = img.copy()
imgContours = img.copy()
blurImage = cv.GaussianBlur(grayImage,(5, 5), 1)
cannyImage = cv.Canny(blurImage,10,70)
threshImage  =  cv.threshold(grayImage, 150,255,cv.THRESH_BINARY_INV)[1]
# threshImage2  =  cv.threshold(grayImage, 150,255,cv.THRESH_BINARY_INV)[1]
# utlis.splitBoxes(threshImage)

contours, hierarchy = cv.findContours(cannyImage, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_NONE) # FIND ALL CONTOURS
cv.drawContours(imgContours, contours, -1, (0, 255, 0), 1) 

rectCon = utlis.rectContour(contours) # FILTER FOR RECTANGLE CONTOURS
biggestPoints= utlis.getCornerPoints(rectCon[0]) # GET CORNER POINTS OF THE BIGGEST RECTANGLE
#gradePoints = utlis.getCornerPoints(rectCon[1]) # GET CORNER POINTS OF THE SECOND BIGGEST RECTANGLE
if biggestPoints.size != 0:
    # print("working inside if block")
    biggestPoints=utlis.reorder(biggestPoints) # REORDER FOR WARPING
    cv.drawContours(imgBigContour, biggestPoints, -1, (0, 255, 0), 20) # DRAW THE BIGGEST CONTOUR
    pts1 = np.float32(biggestPoints) # PREPARE POINTS FOR WARP
    pts2 = np.float32([[0, 0],[widthImg, 0], [0, heightImg],[widthImg, heightImg]]) # PREPARE POINTS FOR WARP
    matrix = cv.getPerspectiveTransform(pts1, pts2) # GET TRANSFORMATION MATRIX
    imgWarpColored = cv.warpPerspective(img, matrix, (widthImg, heightImg))
    # cv.imshow("imgWarpColored", imgWarpColored)
    # imageArray =[ [img,grayImage,threshImage] ,[imgContours,imgWarpColored,blankImage]]
    # allImages = utlis.stackImages(imageArray,1)


    imgWarpGray = cv.cvtColor(imgWarpColored,cv.COLOR_BGR2GRAY) # CONVERT TO GRAYSCALE
    imgThresh = cv.threshold(imgWarpGray, 170, 255,cv.THRESH_BINARY_INV )[1] # APPLY THRESHOLD AND INVERSE


    imageArray =[imgWarpColored,imgWarpGray,imgThresh]
    allImages = utlis.stackImages(imageArray,1)
    cv.imshow("All Images",allImages )
    # boxes = utlis.splitBoxes(imgThresh) 
    # utlis.splitBoxes(imgThresh) 
    boxes = []
    boxes = utlis.splitBoxes2(imgThresh)
    # utlis.splitBoxes(imgThresh)
    # utlis.splitBoxes2(imgThresh)
    # print(boxes.size())


    countR=0
    countC=0
    myPixelVal = np.zeros((11,10)) # TO STORE THE NON ZERO VALUES OF EACH BOX , ten rows and 11 columns
    #! notes: burad np.zeros((10,11)) mi yoksa np.zeros((11,10)) olmasi gerekmektedir.
    # print(myPixelVal)
    for image in boxes:
        #cv2.imshow(str(countR)+str(countC),image)
        totalPixels = cv.countNonZero(image)
        myPixelVal[countC][countR]= totalPixels
        countR += 1
        if (countR==10):countR=0;countC +=1

    myIndex=[]
    for x in range (0,11):
        arr = myPixelVal[x]
        myIndexVal = np.where(arr == np.amax(arr))
        myIndex.append(myIndexVal[0][0])
    # print(myIndex)
    final_result = ''.join([str(elem) for elem in myIndex]) 
    print("Ogrencinin kimlik numarasi: ",final_result)
    
    cv.waitKey(0)

