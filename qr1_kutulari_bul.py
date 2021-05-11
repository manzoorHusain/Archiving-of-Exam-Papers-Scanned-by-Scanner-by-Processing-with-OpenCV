import cv2
mypath = "C:\\Users\\zaida\\Desktop\\Bitirme_proje_Denemeler\\qr1.png"
img = cv2.imread(mypath, 0)
cv2.imshow('test', img)


cv2.waitKey(0)
cv2.destroyAllWindows()

not_kutu = img[118:230 ,1168:1535]
sinav_girme_kutu = img[245:295,1168:1535]
cv2.imshow('Not kutusu', not_kutu)
cv2.waitKey(0)
cv2.destroyAllWindows()
cv2.imshow('sinav_girme_kutu', sinav_girme_kutu)
cv2.waitKey(0)
cv2.destroyAllWindows()