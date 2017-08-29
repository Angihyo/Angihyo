import cv2 
import numpy as np

img = cv2.imread('sign2.jpg', cv2.IMREAD_COLOR)
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
edges = cv2.Canny(gray,40,140)
while(1):
    #img 카피하기.
    img2 = img.copy()
    #img2 가우시안 블러 처리.
    img2 = cv2.GaussianBlur(img2, (3,3), 0)
    #img2 그레이 처리.
    gray2 = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)

    #원형 허프변환 : parmar1,2 조절이 핵심포인트.
    circles = cv2.HoughCircles(gray2, cv2.HOUGH_GRADIENT, 1, 10, param1=200, param2=120, minRadius=0, maxRadius=0)  

    if circles is not None:
        circles = np.uint16(np.around(circles))
        for i in circles[0, :]:
            #원그리기 (img2,  원중심    , 반지름, 선 색깔,   선 두께)
            cv2.circle(img2, (i[0], i[1]), i[2], (255, 255, 0), 3)  
            #허프변환으로 잡은 값 체크. 
            print(i[0]) # X값
            print(i[1]) # Y값
            print(i[2]) # 반지름값
            #crop 하기.      [ y-반지름 : y+반지름까지, x-반지름 : x+반지름]
            crop_cimg1 = gray[i[1]-i[2] : i[1]+i[2] ,   i[0]-i[2] : i[0]+i[2]] #crop from x, y, w, h 

    #이미지출력 : 원본, 허프잡은것, crop한것.
    cv2.imshow('original', img)
    cv2.imshow('Circle', img2)
    cv2.imshow('crop circle',crop_cimg1)

    cv2.waitKey(0)

cv2.destroyAllWindows() 

