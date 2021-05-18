import cv2 as cv
import numpy as np
import utlis

img = cv.imread('Photos/qr2-1.png')
gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)

width = 900
height = 1200
img = cv.resize(img, (width, height))
imgC = cv.resize(img, (width, height))
img = imgC[:, width//2:width-1]
output = img.copy()
gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
blur = cv.GaussianBlur(gray, (5, 5), 1)
canny = cv.Canny(blur, 10, 15)


# kagitaki dikdortgenleri bulma
contours, hierarchy = cv.findContours(
    canny, cv.RETR_EXTERNAL,
    cv.CHAIN_APPROX_NONE)
# kagitaki dikdortgenleri cizme
index = None
for i, c in enumerate(contours):
    # alan
    if cv.contourArea(c) > 900:
        cv.drawContours(img, contours, i, (255, 0, 255), 2)
        index = i
        # print(cv.contourArea(c))

        # print(len(cv.approxPolyDP(c, cv.arcLength(c, True)*0.1, True)))
mask = np.zeros_like(img)
# cv.imshow('img', img)

cv.drawContours(mask, contours, index, (255, 255, 255), -1)
# cv.imshow('mask2', mask)

# istenilen kutuyu cikarmak
output = np.zeros_like(img)
# cv.imshow('output1', output)

output[mask == 255] = img[mask == 255]
# cv.imshow('output3', output)  # sadece kimlik numarali olan kisim ama buturn resmin icerisinde


# o kutu icin resimde crop yapmak
(y, x) = np.where(mask == 255)[:2]
(topy, topx) = (np.min(y), np.min(x))
(bottomy, bottomx) = (np.max(y), np.max(x))
output = output[topy:bottomy+1, topx:bottomx+1]
new_img = output.copy() # bu resimde iki bolum var, biri kimligin elle yazildigi ve kodlandigi kisim
# cv.imshow("new image", new_img)


# added later
widthImg = 300
heightImg = 300
questions = 11
# img = cv.imread('Photos/new_image.jpg')
# img = new.copy()
new_img = cv.resize(new_img, (widthImg, heightImg))
# cv.imshow("new image", new_img)
contoursImage = new_img.copy()
grayImage = cv.cvtColor(new_img, cv.COLOR_RGB2BGR)# gray image
blankImage = np.zeros_like(new_img) # blank image
imgBigContour = new_img.copy()
imgContours = new_img.copy()
blurImage = cv.GaussianBlur(grayImage,(5, 5), 1)
cannyImage = cv.Canny(blurImage,10,70)
threshImage  =  cv.threshold(grayImage, 150,255,cv.THRESH_BINARY_INV)[1]

print("Thresh size: ",len(threshImage.shape))

contours, hierarchy = cv.findContours(cannyImage, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_NONE) # FIND ALL CONTOURS
cv.drawContours(imgContours, contours, -1, (0, 255, 0), 1) 

rectCon = utlis.rectContour(contours) # FILTER FOR RECTANGLE CONTOURS
biggestPoints= utlis.getCornerPoints(rectCon[0]) # GET CORNER POINTS OF THE BIGGEST RECTANGLE
if biggestPoints.size != 0:
    # print("working inside if block")
    biggestPoints=utlis.reorder(biggestPoints) # REORDER FOR WARPING
    cv.drawContours(imgBigContour, biggestPoints, -1, (0, 255, 0), 20) # DRAW THE BIGGEST CONTOUR
    pts1 = np.float32(biggestPoints) # PREPARE POINTS FOR WARP
    pts2 = np.float32([[0, 0],[widthImg, 0], [0, heightImg],[widthImg, heightImg]]) # PREPARE POINTS FOR WARP
    matrix = cv.getPerspectiveTransform(pts1, pts2) # GET TRANSFORMATION MATRIX
    imgWarpColored = cv.warpPerspective(new_img, matrix, (widthImg, heightImg))



    imgWarpGray = cv.cvtColor(imgWarpColored,cv.COLOR_BGR2GRAY) # CONVERT TO GRAYSCALE
    imgThresh = cv.threshold(imgWarpGray, 170, 255,cv.THRESH_BINARY_INV )[1] # APPLY THRESHOLD AND INVERSE

    print("thresh size",len(imgThresh.shape))
    imageArray =[new_img,imgWarpColored,imgWarpGray,imgThresh]
    allImages = utlis.stackImages(imageArray,1)
    cv.imshow("All Images",allImages )
    boxes = []
    boxes = utlis.splitBoxes(imgThresh)



    countR=0
    countC=0
    myPixelVal = np.zeros((11,10)) # TO STORE THE NON ZERO VALUES OF EACH BOX , ten rows and 11 columns
    #! notes: burad np.zeros((10,11)) mi yoksa np.zeros((11,10)) olmasi gerekmektedir.
    # print(myPixelVal)
    cv.imshow('First image',boxes[0])
    cv.imshow('11th  image',boxes[1])
    cv.imshow('12th image',boxes[11])
    cv.imshow('13th image',boxes[12])
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

#................................................................
