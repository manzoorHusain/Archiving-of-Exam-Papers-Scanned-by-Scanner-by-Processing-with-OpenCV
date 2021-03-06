import cv2 as cv
import numpy as np
from . import utils
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
    # cv.imshow("new image", new_img)
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
        allImages = utils.stackImages(imageArray, 1)
        # cv.imshow("All Images", allImages)
        boxes = []
        boxes = utils.splitBoxes(imgThresh)

        countR = 0
        countC = 0
        # TO STORE THE NON ZERO VALUES OF EACH BOX , ten rows and 11 columns
        myPixelVal = np.zeros((11, 10))
        #! notes: burad np.zeros((10,11)) mi yoksa np.zeros((11,10)) olmasi gerekmektedir.
        # print(myPixelVal)
        for image in boxes:
            # cv2.imshow(str(countR)+str(countC),image)
            totalPixels = cv.countNonZero(image)
            myPixelVal[countC][countR] = totalPixels
            countR += 1
            if (countR == 10):
                countR = 0
                countC += 1

        myIndex = []
        for x in range(0, 11):
            arr = myPixelVal[x]
            myIndexVal = np.where(arr == np.amax(arr))
            myIndex.append(myIndexVal[0][0])
        # print(myIndex)
        final_result = ''.join([str(elem) for elem in myIndex])
        # print("Ogrencinin kimlik numarasi: ", final_result)

    cv.waitKey(0)
    return final_result


all_thresh_images = []
all_gray_images = []
global_counter = 0


def get_tc(img):
    gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)

    width = 900
    height = 1200
    img = cv.resize(img, (width, height))
    img_coppied = cv.resize(img, (width, height))
    img = img_coppied[:, width//2:width-1]
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
    width_img = 300
    height_img = 300
    questions = 11
    # img = cv.imread('Photos/new_image.jpg')
    # img = new.copy()
    new_img = cv.resize(new_img, (width_img, height_img))
    # cv.imshow("new image", new_img)
    # contoursImage = new_img.copy()
    gray_img = cv.cvtColor(new_img, cv.COLOR_RGB2BGR)  # gray image
    blank_img = np.zeros_like(new_img)  # blank image
    big_contour_img = new_img.copy()
    contour_img = new_img.copy()
    blur_img = cv.GaussianBlur(gray_img, (5, 5), 1)
    blur_img = cv.Canny(blur_img, 10, 70)
    # threshImage = cv.threshold(gray_img, 150, 255, cv.THRESH_BINARY_INV)[1]

    contours, hierarchy = cv.findContours(
        blur_img, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_NONE)  # FIND ALL CONTOURS
    cv.drawContours(contour_img, contours, -1, (0, 255, 0), 1)

    rec_contour = utils.rectContour(contours)  # FILTER FOR RECTANGLE CONTOURS
    # GET CORNER POINTS OF THE BIGGEST RECTANGLE
    # all_thresh_images = []
    biggest_points = utils.getCornerPoints(rec_contour[0])
    if biggest_points.size != 0:
        # print("working inside if block")
        biggest_points = utils.reorder(biggest_points)  # REORDER FOR WARPING
        cv.drawContours(big_contour_img, biggest_points, -1,
                        (0, 255, 0), 20)  # DRAW THE BIGGEST CONTOUR
        pts1 = np.float32(biggest_points)  # PREPARE POINTS FOR WARP
        pts2 = np.float32([[0, 0], [width_img, 0], [0, height_img], [
                          width_img, height_img]])  # PREPARE POINTS FOR WARP
        matrix = cv.getPerspectiveTransform(
            pts1, pts2)  # GET TRANSFORMATION MATRIX
        warp_colored_img = cv.warpPerspective(
            new_img, matrix, (width_img, height_img))

        warp_gray_img = cv.cvtColor(
            warp_colored_img, cv.COLOR_BGR2GRAY)  # CONVERT TO GRAYSCALE
        thresh_img = cv.threshold(warp_gray_img, 170, 255, cv.THRESH_BINARY_INV)[
            1]  # APPLY THRESHOLD AND INVERSE

        image_arry = [new_img, warp_colored_img, warp_gray_img, thresh_img]

        # cv.imshow("thresh image",thresh_img)
        # global_counter += 1
        # all_thresh_images[0] = all_thresh_images.append(thresh_img)

        all_thresh_images.append(thresh_img)
        all_gray_images.append(warp_gray_img)

        # cv.imwrite("Photos/small_image.jpg",warp_colored_img)
        all_images = utils.stack_images(image_arry, 1)
        # cv.imshow("All Images", all_images)
        # cv.imshow("before cropping",thresh_img)

        thresh_img = thresh_img[0:height_img - 10, :]
        # print(thresh_img.shape[1])
        # cv.imshow("After cropping",thresh_img)
        boxes = []
        # 110 tane ayri ayri kutu(resim dikdortgenleri seklinde)
        boxes = utils.splitBoxes(thresh_img)
        # print(len(boxes)) # total length is 110
        # allBoxes = []
        # box1 = boxes[7]
        count_percentage = 0
        for i, img in enumerate(boxes):
            width = img.shape[0]  # width
            length = img.shape[1]
            white_pixel = np.sum(img == 255)
            black_pixel = np.sum(img == 0)
            # white_percentage = (white_pixel/ (width*length)) *100
            # (white_pixel/ (width*length)) *100
            white_percentage = (white_pixel*100)/468
            if white_percentage > 80:
                # print(white_percentage)
                count_percentage += 1
                # cv.imshow("image"+str(i), img)
        # print("\ntotal percentage counter",count_percentage)
        print("")
        if count_percentage != 11:
            if count_percentage == 0:
                final_result = "Completely blank"
            elif count_percentage > 11:
                final_result = "Coded more than 11 times"
            else:
                final_result = "Not coded properly"
            return final_result

        count_row = 0
        count_col = 0

        # TO STORE THE NON ZERO VALUES OF EACH BOX , ten rows and 11 columns
        my_pixel_val = np.zeros((11, 10))
        #! notes: burad np.zeros((10,11)) mi yoksa np.zeros((11,10)) olmasi gerekmektedir.
        # print(my_pixel_val)
        # white_percentages = []
        for image in boxes:
            width = image.shape[0]
            length = image.shape[1]
            # cv2.imshow(str(count_row)+str(count_col),image)
            total_pixel = cv.countNonZero(image)  # beyaz pixel
            # white_percentages.append((total_pixel/ (width*length)) *100)
            my_pixel_val[count_col][count_row] = total_pixel
            # print(total_pixel)
            count_row += 1
            if (count_row == 10):
                count_row = 0
                count_col += 1
        my_index = []
        for x in range(0, 11):
            arr = my_pixel_val[x]
            # returns the index of max value.
            my_index_val = np.where(arr == np.amax(arr))
            # print(my_index_val)
            my_index.append(my_index_val[0][0])

        final_result = ''.join([str(elem) for elem in my_index])
    return final_result
