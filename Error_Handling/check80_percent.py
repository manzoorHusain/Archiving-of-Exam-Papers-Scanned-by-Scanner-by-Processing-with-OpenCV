import cv2 as cv
import numpy as np
import utils
from pyzbar import pyzbar


def get_qrcode(img):
    barkodlar = pyzbar.decode(img)
    for barkod in barkodlar:
        (x, y, w, h) = barkod.rect
        cv.rectangle(img, (x, y), (x + w, y + h), (100, 50, 250), 2)

        qrBilgi = barkod.data.decode('utf-8')
        barkodTipi = barkod.type
        text = "{} ( {} )".format(qrBilgi, barkodTipi)
        cv.putText(img, text, (x, y - 15),
                   cv.FONT_HERSHEY_COMPLEX, 0.5, (100, 50, 250), 2)

        # print("barkodtan Cikarilan bilgiler : \n barkod tipi: {}\n barkod icindeki bilgi : \n{}".format(
        # barkodTipi, qrBilgi))
    # cv.imshow("img", img)
    return qrBilgi


def get_tc(img):
    # img = cv.imread('Photos/qr2-1.png')
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
    # bu resimde iki bolum var, biri kimligin elle yazildigi ve kodlandigi kisim
    new_img = output.copy()
    # cv.imshow("new image", new_img)

    # added later
    widthImg = 300
    heightImg = 300
    questions = 11
    # img = cv.imread('Photos/new_image.jpg')
    # img = new.copy()
    new_img = cv.resize(new_img, (widthImg, heightImg))
    cv.imshow("new image", new_img)
    contoursImage = new_img.copy()
    grayImage = cv.cvtColor(new_img, cv.COLOR_RGB2BGR)  # gray image
    blankImage = np.zeros_like(new_img)  # blank image
    imgBigContour = new_img.copy()
    imgContours = new_img.copy()
    blurImage = cv.GaussianBlur(grayImage, (5, 5), 1)
    cannyImage = cv.Canny(blurImage, 10, 70)
    threshImage = cv.threshold(grayImage, 150, 255, cv.THRESH_BINARY_INV)[1]

    contours, hierarchy = cv.findContours(
        cannyImage, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_NONE)  # FIND ALL CONTOURS
    cv.drawContours(imgContours, contours, -1, (0, 255, 0), 1)

    rectCon = utils.rectContour(contours)  # FILTER FOR RECTANGLE CONTOURS
    # GET CORNER POINTS OF THE BIGGEST RECTANGLE
    biggestPoints = utils.getCornerPoints(rectCon[0])
    if biggestPoints.size != 0:
        # print("working inside if block")
        biggestPoints = utils.reorder(biggestPoints)  # REORDER FOR WARPING
        cv.drawContours(imgBigContour, biggestPoints, -1,
                        (0, 255, 0), 20)  # DRAW THE BIGGEST CONTOUR
        pts1 = np.float32(biggestPoints)  # PREPARE POINTS FOR WARP
        pts2 = np.float32([[0, 0], [widthImg, 0], [0, heightImg], [
            widthImg, heightImg]])  # PREPARE POINTS FOR WARP
        matrix = cv.getPerspectiveTransform(
            pts1, pts2)  # GET TRANSFORMATION MATRIX
        imgWarpColored = cv.warpPerspective(
            new_img, matrix, (widthImg, heightImg))

        imgWarpGray = cv.cvtColor(
            imgWarpColored, cv.COLOR_BGR2GRAY)  # CONVERT TO GRAYSCALE
        imgThresh = cv.threshold(imgWarpGray, 170, 255, cv.THRESH_BINARY_INV)[
            1]  # APPLY THRESHOLD AND INVERSE

        imageArray = [new_img, imgWarpColored, imgWarpGray, imgThresh]
        # cv.imwrite("Photos/small_image.jpg",imgWarpColored)
        allImages = utils.stackImages(imageArray, 1)
        cv.imshow("All Images", allImages)
        # cv.imshow("before cropping",imgThresh)

        imgThresh = imgThresh[0:heightImg -10,:]
        # print(imgThresh.shape[1])
        # cv.imshow("After cropping",imgThresh)
        boxes = []
        boxes = utils.splitBoxes(imgThresh) # 110 tane ayri ayri kutu(resim dikdortgenleri seklinde)
        # print(len(boxes)) # total length is 110
        allBoxes = []
        box1 = boxes[7]
        count_percentage = 0
        for i,img in  enumerate(boxes):
            width = img.shape[0] #width
            length = img.shape[1]
            white_pixel = np.sum(img == 255) 
            black_pixel = np.sum(img == 0)
            # white_percentage = (white_pixel/ (width*length)) *100
            white_percentage = (white_pixel*100)/468#(white_pixel/ (width*length)) *100
            if white_percentage  > 80:
                print(white_percentage)
                count_percentage +=1
                cv.imshow("image"+str(i),img)
        # print("totala percentage counter",count_percentage)

        # print(box1.shape[0])
        # print(box1.shape[1])
        # cv.imshow("image",box1)
        width = box1.shape[0] #width
        length = box1.shape[1] # height
        print(width,length)
        box2 = boxes[1]
        box3 = boxes[2]
        countPixels1 = cv.countNonZero(box1) # white_pixels
        countPixels2 = cv.countNonZero(box2)# white_pixels
        countPixels3 = cv.countNonZero(box3)# white_pixels
        white_pixel = np.sum(box1 == 255) 
        black_pixel = np.sum(box1 == 0)
        white_percentage = (white_pixel/ (width*length)) *100
        black_percentage = (black_pixel/ (width*length)) *100
        print("white percentage: ",white_percentage)
        print("black percentage: ",black_percentage)
        print("Total percentage: ",white_percentage+black_percentage)
        # print(countPixels1, countPixels2, countPixels3)
        # print("White pixel: ", white_pixel,"black_pixel",black_pixel)

        # print(len(someBoxes))
        # cv.imshow("img",someBoxes)
        # allBoxesCombined = utils.stackImages(someBoxes,0.2)
        # cv.imshow("All boxes",allBoxesCombined)
        # j = 0
        # for i in range(len(boxes)):
        #     print(f'boxes[{i}],',end='')
        #     j += 1
        #     if j ==10:
        #         print("")
        #         j = 0
        # utils.stackImages([allBoxes], 1)
        # boxImg = (boxes[0]).copy()
        # cv.imshow("boxImage", boxImg)
        countR = 0
        countC = 0
        
        # TO STORE THE NON ZERO VALUES OF EACH BOX , ten rows and 11 columns
        myPixelVal = np.zeros((11, 10)) 
        #! notes: burad np.zeros((10,11)) mi yoksa np.zeros((11,10)) olmasi gerekmektedir.
        # print(myPixelVal)
        white_percentages = []
        for image in boxes:
            width = image.shape[0]
            length = image.shape[1]
            # cv2.imshow(str(countR)+str(countC),image)
            totalPixels = cv.countNonZero(image) # beyaz pixel
            # white_percentages.append((totalPixels/ (width*length)) *100)
            myPixelVal[countC][countR] = totalPixels 
            # print(totalPixels)
            countR += 1
            if (countR == 10):
                countR = 0
                countC += 1
        # print(totalPixels)
        # print("White percentages: ",white_percentages)
        myIndex = []
        for x in range(0, 11):# [[1,1,e4,4],[],[]] print(arr[0][0])
            arr = myPixelVal[x]
            # arr = [[],[],[],[]]
            # print(arr)
            myIndexVal = np.where(arr == np.amax(arr)) # returns the index of max value.
            # print(myIndexVal) 
            myIndex.append(myIndexVal[0][0])
        # print(myIndex) # list of kimlik no
        print(myIndex)
        final_result = ''.join([str(elem) for elem in myIndex])
        # print("Ogrencinin kimlik numarasi: ", final_result)

    # cv.waitKey(0)
    return final_result


width = 900
height = 1200
images = []
# img = cv.imread('Photos/1.png')
# img = cv.resize(img, (width, height))
# images.append(img)
img = cv.imread('Photos/3.png')
# img = cv.resize(img, (width, height))
# images.append(img)
# img = cv.imread('Photos/3.png')
# img = cv.resize(img, (width, height))
# images.append(img)
# img = cv.imread('Photos/4.png')
img = cv.resize(img, (width, height))
images.append(img)


for i, im in enumerate(images):
    # print(i+1, " resim")
    tc = get_tc(im)
    print("tc: ", tc)
    qr_code = get_qrcode(im)
    # print("qr_code: ", qr_code)

stakImages = utils.stackImages([images],0.3)

# cv.imshow("All images",stakImages)
cv.waitKey(0)
        # 110 kutumuz

        # allBoxes = [
        #     [boxes[0],boxes[1],boxes[2],boxes[3],boxes[4],boxes[5],boxes[6],boxes[7],boxes[8],boxes[9]],
        #     [boxes[10],boxes[11],boxes[12],boxes[13],boxes[14],boxes[15],boxes[16],boxes[17],boxes[18],boxes[19]],
        #     [boxes[20],boxes[21],boxes[22],boxes[23],boxes[24],boxes[25],boxes[26],boxes[27],boxes[28],boxes[29]],
        #     [boxes[30],boxes[31],boxes[32],boxes[33],boxes[34],boxes[35],boxes[36],boxes[37],boxes[38],boxes[39]],
        #     [boxes[40],boxes[41],boxes[42],boxes[43],boxes[44],boxes[45],boxes[46],boxes[47],boxes[48],boxes[49]],
        #     [boxes[50],boxes[51],boxes[52],boxes[53],boxes[54],boxes[55],boxes[56],boxes[57],boxes[58],boxes[59]],
        #     [boxes[60],boxes[61],boxes[62],boxes[63],boxes[64],boxes[65],boxes[66],boxes[67],boxes[68],boxes[69]],
        #     [boxes[70],boxes[71],boxes[72],boxes[73],boxes[74],boxes[75],boxes[76],boxes[77],boxes[78],boxes[79]],
        #     [boxes[80],boxes[81],boxes[82],boxes[83],boxes[84],boxes[85],boxes[86],boxes[87],boxes[88],boxes[89]],
        #     [boxes[90],boxes[91],boxes[92],boxes[93],boxes[94],boxes[95],boxes[96],boxes[97],boxes[98],boxes[99]],
        #     [boxes[100],boxes[101],boxes[102],boxes[103],boxes[104],boxes[105],boxes[106],boxes[107],boxes[108],boxes[109]]
        # ]
    
