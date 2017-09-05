# -*- coding: cp949 -*-
# -*- coding: utf-8 -*- # �ѱ� �ּ������� �̰� �ؾ���
import cv2 # opencv ���
import numpy as np

def grayscale(img): # ����̹����� ��ȯ
    return cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)

def canny(img, low_threshold, high_threshold): # Canny �˰���
    return cv2.Canny(img, low_threshold, high_threshold)

def gaussian_blur(img, kernel_size): # ����þ� ����
    return cv2.GaussianBlur(img, (kernel_size, kernel_size), 0)

def region_of_interest(img, vertices, color3=(255,255,255), color1=255): # ROI ����

    mask = np.zeros_like(img) # mask = img�� ���� ũ���� �� �̹���
    
    if len(img.shape) > 2: # Color �̹���(3ä��)��� :
        color = color3
    else: # ��� �̹���(1ä��)��� :
        color = color1
        
    # vertices�� ���� ����� �̷��� �ٰ����κ�(ROI �����κ�)�� color�� ä�� 
    cv2.fillPoly(mask, vertices, color)
    
    # �̹����� color�� ä���� ROI�� ��ħ
    ROI_image = cv2.bitwise_and(img, mask)
    return ROI_image

def draw_lines(img, lines, color=[255, 0, 0], thickness=2): # �� �׸���
    for line in lines:
        for x1,y1,x2,y2 in line:
            cv2.line(img, (x1, y1), (x2, y2), color, thickness)

def draw_fit_line(img, lines, color=[255, 0, 0], thickness=10): # ��ǥ�� �׸���
        cv2.line(img, (lines[0], lines[1]), (lines[2], lines[3]), color, thickness)

def hough_lines(img, rho, theta, threshold, min_line_len, max_line_gap): # ���� ��ȯ
    lines = cv2.HoughLinesP(img, rho, theta, threshold, np.array([]), minLineLength=min_line_len, maxLineGap=max_line_gap)
    #line_img = np.zeros((img.shape[0], img.shape[1], 3), dtype=np.uint8)
    #draw_lines(line_img, lines)

    return lines

def weighted_img(img, initial_img, ��=1, ��=1., ��=0.): # �� �̹��� operlap �ϱ�
    return cv2.addWeighted(initial_img, ��, img, ��, ��)

def get_fitline(img, f_lines): # ��ǥ�� ���ϱ�   
    lines = np.squeeze(f_lines)
    #print(lines)
    #print(lines.shape[0])
    lines = lines.reshape(lines.shape[0]*2,2)
    #print(lines.shape[0])
    rows,cols = img.shape[:2]
    output = cv2.fitLine(lines,cv2.DIST_L2,0, 0.01, 0.01)
    vx, vy, x, y = output[0], output[1], output[2], output[3]
    x1, y1 = int(((img.shape[0]-1)-y)/vy*vx + x) , img.shape[0]-1
    x2, y2 = int(((img.shape[0]/2+100)-y)/vy*vx + x) , int(img.shape[0]/2+100)
    
    result = [x1,y1,x2,y2]
    return result
def ransac_vanishing_point_detection(lines, distance=50, iterations=100):
    """
    Calculate the vanishing point of the road markers.
    :param lines: the lines defined as a [x1, y1, x2, y2] (4xN array, where N is the number of lines)
    :param distance: the distance (in pixels) to determine if a measurement is consistent
    :param iterations: the number of RANSAC iterations to use
    :return: Coordinates of the road vanishing point
    """

    # Number of lines
    N = len(lines)

    # Maximum number of consistant lines
    max_num_consistent_lines = 0

    # Best fit point
    best_fit = None

    # Loop through all of the iterations to find the most consistent value
    for i in range(0, iterations):

        # Randomly choosing the lines
        random_indices = np.random.choice(N, 2, replace=False)
        i1 = random_indices[0]
        i2 = random_indices[1]
        x1, y1, x2, y2 = lines[i1]
        x3, y3, x4, y4 = lines[i2]

        # Find the intersection point
        try:
            x_intersect = ((x1*y2-y1*x2)*(x3-x4)-(x1-x2)*(x3*y4-y3*x4))/((x1-x2)*(y3-y4)-(y1-y2)*(x3-x4))
            y_intersect = ((x1*y2-y1*x2)*(y3-y4)-(y1-y2)*(x3*y4-y3*x4))/((x1-x2)*(y3-y4)-(y1-y2)*(x3-x4))
        except :
            pass
        if y_intersect < 80 or y_intersect > 300:
            continue

        this_num_consistent_lines = 0

        # Find the distance between the intersection and all of the other lines
        for i2 in range(0, N):

            tx1, ty1, tx2, ty2 = lines[i2]
            this_distance = (np.abs((ty2-ty1)*x_intersect - (tx2-tx1)*y_intersect + tx2*ty1 - ty2*tx1)
                             / np.sqrt((ty2-ty1)**2 + (tx2-tx1)**2))

            if this_distance < distance:
                this_num_consistent_lines += 1

        # If it's greater, make this the new x, y intersect
        if this_num_consistent_lines > max_num_consistent_lines:
            best_fit = int(x_intersect), int(y_intersect)
            max_num_consistent_lines = this_num_consistent_lines

    return best_fit

######################################### 9.5 �������� def �߰���.
def CircleDetecting(img1):
    #img ī���ϱ�.
    img2 = img1.copy()
    #img2 ����þ� �� ó��. (������ def �� ����)
    img2 = gaussian_blur(img2, 3)
    #img2 �׷��� ó��. (������ def�� ����)
    gray2 = grayscale(img2)

    #���� ������ȯ : parmar1,2 ������ �ٽ�����Ʈ.
    circles = cv2.HoughCircles(gray2, cv2.HOUGH_GRADIENT, 1, 10, param1=200, param2=120, minRadius=0, maxRadius=0)  

    if circles is not None:
        circles = np.uint16(np.around(circles))
        for i in circles[0, :]:
            #���׸��� (img2,  ���߽�    , ������, �� ����,   �� �β�)
            cv2.circle(img2, (i[0], i[1]), i[2], (255, 255, 0), 3)  
            #������ȯ���� ���� �� üũ. 
            print(i[0]) # X��
            print(i[1]) # Y��
            print(i[2]) # ��������
            #crop �ϱ�.      [ y-������ : y+����������, x-������ : x+������]
            crop_cimg1 = gray[i[1]-i[2] : i[1]+i[2] ,   i[0]-i[2] : i[0]+i[2]] #crop from x, y, w, h 

    ##�̹������ : ����, ����������, crop�Ѱ�.
    # cv2.imshow('original', img)
    # cv2.imshow('Circle', img2)
    # cv2.imshow('crop circle',crop_cimg1)

    #cv2.waitKey(0)
#########################################
def LineDetecting(img1):
    image = img1 # �̹��� �б�

    height, width = image.shape[:2] # �̹��� ����, �ʺ�
    #print(height)
    #print(width)

    gray_img = grayscale(image) # ����̹����� ��ȯ
        
    blur_img = gaussian_blur(gray_img, 3) # Blur ȿ��
       
    canny_img = canny(blur_img, 70, 210) # Canny edge �˰���

    vertices = np.array([[(0,height),(width/2-100, height/2+80), (width/2+100, height/2+80), (width,height)]], dtype=np.int32)
    ROI_img = region_of_interest(canny_img, vertices) # ROI ����

    line_arr = hough_lines(ROI_img, 1, 1 * np.pi/180, 30, 10, 20) # ���� ��ȯ
    line_arr = np.squeeze(line_arr)
    #print(line_arr)    
    # ���� ���ϱ�
    slope_degree = (np.arctan2(line_arr[:,1] - line_arr[:,3], line_arr[:,0] - line_arr[:,2]) * 180) / np.pi
    #print(slope_degree)
    # ���� ���� ����
    line_arr = line_arr[np.abs(slope_degree)<170]
    slope_degree = slope_degree[np.abs(slope_degree)<170]
    #print(line_arr)
    #print(slope_degree)
    # ���� ���� ����
    line_arr = line_arr[np.abs(slope_degree)>95]
    slope_degree = slope_degree[np.abs(slope_degree)>95]
    #print(line_arr)
    #print(slope_degree)
    # ���͸��� ���� ������
    L_lines, R_lines = line_arr[(slope_degree>0),:], line_arr[(slope_degree<0),:]
    #print(L_lines)
    #print(R_lines)
    temp = np.zeros((image.shape[0], image.shape[1], 3), dtype=np.uint8)
    L_lines, R_lines = L_lines[:,None], R_lines[:,None]
    #print(L_lines)
    #print(R_lines)
    # ����, ������ ���� ��ǥ�� ���ϱ�
    left_fit_line = get_fitline(image,L_lines)
    right_fit_line = get_fitline(image,R_lines)
    # ��ǥ�� �׸���
    draw_fit_line(temp, left_fit_line)
    draw_fit_line(temp, right_fit_line)
    # �ҽ��� ã��
    vanishing_point = ransac_vanishing_point_detection(line_arr)
    print(vanishing_point)
    #cv2.imshow('point',vanishing_point)
    #cv2.plot(vanishing_point)


    result = weighted_img(temp, image) # ���� �̹����� ����� �� overlap
    cv2.imshow('result',result) # ��� �̹��� ���
