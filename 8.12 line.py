import cv2 
import numpy as np
 

img = cv2.imread('sign3.jpg', cv2.IMREAD_COLOR)
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
edges = cv2.Canny(gray,40,140)
while(1):
    
    cv2.imshow('original', img)
    cv2.imshow('gray',gray)
    
    lines = cv2.HoughLinesP(edges, 1, np.pi / 180, 10, None, 100, 10)

    if lines is not None:
        for line in lines[0]:
            pt1 = (line[0], line[1])
            pt2 = (line[2], line[3])

            cv2.line(img, pt1, pt2, (0, 0, 255), 3)


    cv2.imshow('original', img)
    cv2.imshow('gray',gray)
    cv2.imshow('Edges',edges)
    cv2.waitKey(0)

    

cv2.destroyAllWindows() 
