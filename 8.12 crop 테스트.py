import cv2 
import numpy as np
 

img = cv2.imread('sign30.jpg', cv2.IMREAD_COLOR)
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
edges = cv2.Canny(gray,40,140)
while(1):
    

    
    lines = cv2.HoughLinesP(edges, 1, np.pi / 180, 10, None, 100, 10)

    if lines is not None:
        for line in lines[0]:
            pt1 = (line[0], line[1])
            pt2 = (line[2], line[3])

            cv2.line(edges, pt1, pt2, (0, 0, 255), 3)


    cv2.imshow('original', img)
    #cv2.imshow('gray',gray)
    #cv2.imshow('Edges',edges)

    ##circle detect
    img2 = img.copy()
    img2 = cv2.GaussianBlur(img2, (3,3), 0)
    gray2 = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)
    #parmar1,2 조절이 핵심포인트.
    circles = cv2.HoughCircles(gray2, cv2.HOUGH_GRADIENT, 1, 10, param1=675, param2=120, minRadius=0, maxRadius=0)
    
    if circles is not None:
        circles = np.uint16(np.around(circles))

        for i in circles[0, :]:
            cv2.circle(img2, (i[0], i[1]), i[2], (255, 255, 0), 3)  #3이 두께를 의미.

            cv2.imshow('Circle', img2)

            crop_cimg0 = gray[i[0]:300,i[1]:300] #crop from x, y, w, h
            crop_cimg1 = gray[i[0]-50:300,i[1]-50:320] #crop from x, y, w, h
            crop_cimg2 = gray[i[0]-130:300,i[1]-90:320] #crop from x, y, w, h
            crop_cimg3 = gray[i[0]-100:300,i[1]-100:320] #crop from x, y, w, h
            crop_cimg4 = gray[i[0]-150:300,i[1]-150:320] #crop from x, y, w, h 

    cv2.imshow('0',crop_cimg0)
    cv2.imshow('1',crop_cimg1)
    cv2.imshow('2',crop_cimg2)
    cv2.imshow('3',crop_cimg3)
    cv2.imshow('4',crop_cimg4)


    cv2.waitKey(0)

    

cv2.destroyAllWindows() 

