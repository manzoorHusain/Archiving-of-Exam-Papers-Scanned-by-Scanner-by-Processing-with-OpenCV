import cv2
import numpy as np

# TO STACK ALL THE IMAGES IN ONE WINDOW


def stackImages(imgArray, scale, lables=[]):
    rows = len(imgArray)
    cols = len(imgArray[0])
    rowsAvailable = isinstance(imgArray[0], list)
    width = imgArray[0][0].shape[1]
    height = imgArray[0][0].shape[0]
    if rowsAvailable:
        for x in range(0, rows):
            for y in range(0, cols):
                imgArray[x][y] = cv2.resize(
                    imgArray[x][y], (0, 0), None, scale, scale)
                if len(imgArray[x][y].shape) == 2:
                    imgArray[x][y] = cv2.cvtColor(
                        imgArray[x][y], cv2.COLOR_GRAY2BGR)
        imageBlank = np.zeros((height, width, 3), np.uint8)
        hor = [imageBlank]*rows
        hor_con = [imageBlank]*rows
        for x in range(0, rows):
            hor[x] = np.hstack(imgArray[x])
            hor_con[x] = np.concatenate(imgArray[x])
        ver = np.vstack(hor)
        ver_con = np.concatenate(hor)
    else:
        for x in range(0, rows):
            imgArray[x] = cv2.resize(imgArray[x], (0, 0), None, scale, scale)
            if len(imgArray[x].shape) == 2:
                imgArray[x] = cv2.cvtColor(imgArray[x], cv2.COLOR_GRAY2BGR)
        hor = np.hstack(imgArray)
        hor_con = np.concatenate(imgArray)
        ver = hor
    if len(lables) != 0:
        eachImgWidth = int(ver.shape[1] / cols)
        eachImgHeight = int(ver.shape[0] / rows)
        # print(eachImgHeight)
        for d in range(0, rows):
            for c in range(0, cols):
                cv2.rectangle(ver, (c*eachImgWidth, eachImgHeight*d), (c*eachImgWidth+len(
                    lables[d][c])*13+27, 30+eachImgHeight*d), (255, 255, 255), cv2.FILLED)
                cv2.putText(ver, lables[d][c], (eachImgWidth*c+10, eachImgHeight *
                                                d+20), cv2.FONT_HERSHEY_COMPLEX, 0.7, (255, 0, 255), 2)
    return ver


def reorder(myPoints):

    myPoints = myPoints.reshape((4, 2))  # REMOVE EXTRA BRACKET
    # print(myPoints)
    # NEW MATRIX WITH ARRANGED POINTS
    myPointsNew = np.zeros((4, 1, 2), np.int32)
    add = myPoints.sum(1)
    # print(add)
    # print(np.argmax(add))
    myPointsNew[0] = myPoints[np.argmin(add)]  # [0,0]
    myPointsNew[3] = myPoints[np.argmax(add)]  # [w,h]
    diff = np.diff(myPoints, axis=1)
    myPointsNew[1] = myPoints[np.argmin(diff)]  # [w,0]
    myPointsNew[2] = myPoints[np.argmax(diff)]  # [h,0]

    return myPointsNew


def rectContour(contours):

    rectCon = []
    max_area = 0
    for i in contours:
        area = cv2.contourArea(i)
        if area > 50:
            peri = cv2.arcLength(i, True)
            approx = cv2.approxPolyDP(i, 0.02 * peri, True)
            if len(approx) == 4:
                rectCon.append(i)
    rectCon = sorted(rectCon, key=cv2.contourArea, reverse=True)
    # print(len(rectCon))
    return rectCon


def getCornerPoints(cont):
    peri = cv2.arcLength(cont, True)  # LENGTH OF CONTOUR
    # APPROXIMATE THE POLY TO GET CORNER POINTS
    approx = cv2.approxPolyDP(cont, 0.02 * peri, True)
    return approx


def splitBoxes2(img):
    # rows = np.vsplit(img,10)
    cols = np.vsplit(img, 10)

    # cv2.imshow("first row",rows[9])
    # cv2.imshow("first column",cols[9])
    print(cols)
    boxes = []
    for c in cols:
        print(len(c))

        # rows = np.vsplit(c,10)
        # for r in rows:
        #     boxes.append(r)
        # cv2.imshow('last box',r)
    # boxes=[]
    # for r in rows:
    #     cols= np.hsplit(r,5)
    #     for box in cols:
    #         boxes.append(box)
    # return boxes


def splitBoxes(img):
    # rows = np.vsplit(img,10)
    boxes = []
    cols = []
    cols.append(img[:, 10:img.shape[1]//11])
    # rows = np.vsplit(img,10)
    for i in range(2, 12):
        cols.append(img[:,
                        (i-1)*img.shape[1]//11:i*img.shape[1]//11])
    # cv2.imshow('c0',cols[0])
    for c in cols:
        # print(len(c))
        rows = np.vsplit(c, 10)
        for r in rows:
            boxes.append(r)
            # cv2.imshow('last box',r)
    return boxes

    # cols = np.hsplit(img,11)

    # cv2.imshow("first row",rows[9])
    # c1 = cols[0]
    # c2 = cols[1]
    # cv2.imshow("c0",cols[0])
    # cv2.imshow("c1",cols[1])#tam
    # cv2.imshow("c2",cols[2])#tam degil
    # cv2.imshow("c3",cols[3])#tam degil
    # cv2.imshow("c4",cols[4])# tam degil
    cv2.imshow("c5", cols[5])  # tam degil
    # cv2.imshow("c6",cols[6])# dogru
    # cv2.imshow("c7",cols[7])#dogru
    # cv2.imshow("c8",cols[8]) # dogru
    # cv2.imshow("c9",cols[9]) # dogru

    # imageArray = [c1,c2]
    # stackImages(imageArray,1)


def splitBoxes3(img):
    cols = []
    # rows = np.vsplit(img,10)
    for i in range(2, 12):
        cols.append(img[:,
                        (i-1)*img.shape[1]//11:i*img.shape[1]//11])
    # cols = np.hsplit(img,10)

    cv2.imshow("c5", cols[5])  # tam degil









