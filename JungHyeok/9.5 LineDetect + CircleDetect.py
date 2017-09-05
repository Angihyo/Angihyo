# -*- coding: cp949 -*-
# -*- coding: utf-8 -*- # 한글 주석쓰려면 이거 해야함
import cv2 # opencv 사용
import numpy as np

def grayscale(img): # 흑백이미지로 변환
    return cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)

def canny(img, low_threshold, high_threshold): # Canny 알고리즘
    return cv2.Canny(img, low_threshold, high_threshold)

def gaussian_blur(img, kernel_size): # 가우시안 필터
    return cv2.GaussianBlur(img, (kernel_size, kernel_size), 0)

def region_of_interest(img, vertices, color3=(255,255,255), color1=255): # ROI 셋팅

    mask = np.zeros_like(img) # mask = img와 같은 크기의 빈 이미지
    
    if len(img.shape) > 2: # Color 이미지(3채널)라면 :
        color = color3
    else: # 흑백 이미지(1채널)라면 :
        color = color1
        
    # vertices에 정한 점들로 이뤄진 다각형부분(ROI 설정부분)을 color로 채움 
    cv2.fillPoly(mask, vertices, color)
    
    # 이미지와 color로 채워진 ROI를 합침
    ROI_image = cv2.bitwise_and(img, mask)
    return ROI_image

def draw_lines(img, lines, color=[255, 0, 0], thickness=2): # 선 그리기
    for line in lines:
        for x1,y1,x2,y2 in line:
            cv2.line(img, (x1, y1), (x2, y2), color, thickness)

def draw_fit_line(img, lines, color=[255, 0, 0], thickness=10): # 대표선 그리기
        cv2.line(img, (lines[0], lines[1]), (lines[2], lines[3]), color, thickness)

def hough_lines(img, rho, theta, threshold, min_line_len, max_line_gap): # 허프 변환
    lines = cv2.HoughLinesP(img, rho, theta, threshold, np.array([]), minLineLength=min_line_len, maxLineGap=max_line_gap)
    #line_img = np.zeros((img.shape[0], img.shape[1], 3), dtype=np.uint8)
    #draw_lines(line_img, lines)

    return lines

def weighted_img(img, initial_img, α=1, β=1., λ=0.): # 두 이미지 operlap 하기
    return cv2.addWeighted(initial_img, α, img, β, λ)

def get_fitline(img, f_lines): # 대표선 구하기   
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

######################################### 9.5 원형검출 def 추가함.
def CircleDetecting(img1):
    #img 카피하기.
    img2 = img1.copy()
    #img2 가우시안 블러 처리. (길훈이 def 에 맞춤)
    img2 = gaussian_blur(img2, 3)
    #img2 그레이 처리. (길훈이 def에 맞춤)
    gray2 = grayscale(img2)

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

    ##이미지출력 : 원본, 허프잡은것, crop한것.
    # cv2.imshow('original', img)
    # cv2.imshow('Circle', img2)
    # cv2.imshow('crop circle',crop_cimg1)

    #cv2.waitKey(0)
#########################################
def LineDetecting(img1):
    image = img1 # 이미지 읽기

    height, width = image.shape[:2] # 이미지 높이, 너비
    #print(height)
    #print(width)

    gray_img = grayscale(image) # 흑백이미지로 변환
        
    blur_img = gaussian_blur(gray_img, 3) # Blur 효과
       
    canny_img = canny(blur_img, 70, 210) # Canny edge 알고리즘

    vertices = np.array([[(0,height),(width/2-100, height/2+80), (width/2+100, height/2+80), (width,height)]], dtype=np.int32)
    ROI_img = region_of_interest(canny_img, vertices) # ROI 설정

    line_arr = hough_lines(ROI_img, 1, 1 * np.pi/180, 30, 10, 20) # 허프 변환
    line_arr = np.squeeze(line_arr)
    #print(line_arr)    
    # 기울기 구하기
    slope_degree = (np.arctan2(line_arr[:,1] - line_arr[:,3], line_arr[:,0] - line_arr[:,2]) * 180) / np.pi
    #print(slope_degree)
    # 수평 기울기 제한
    line_arr = line_arr[np.abs(slope_degree)<170]
    slope_degree = slope_degree[np.abs(slope_degree)<170]
    #print(line_arr)
    #print(slope_degree)
    # 수직 기울기 제한
    line_arr = line_arr[np.abs(slope_degree)>95]
    slope_degree = slope_degree[np.abs(slope_degree)>95]
    #print(line_arr)
    #print(slope_degree)
    # 필터링된 직선 버리기
    L_lines, R_lines = line_arr[(slope_degree>0),:], line_arr[(slope_degree<0),:]
    #print(L_lines)
    #print(R_lines)
    temp = np.zeros((image.shape[0], image.shape[1], 3), dtype=np.uint8)
    L_lines, R_lines = L_lines[:,None], R_lines[:,None]
    #print(L_lines)
    #print(R_lines)
    # 왼쪽, 오른쪽 각각 대표선 구하기
    left_fit_line = get_fitline(image,L_lines)
    right_fit_line = get_fitline(image,R_lines)
    # 대표선 그리기
    draw_fit_line(temp, left_fit_line)
    draw_fit_line(temp, right_fit_line)
    # 소실점 찾기
    vanishing_point = ransac_vanishing_point_detection(line_arr)
    print(vanishing_point)
    #cv2.imshow('point',vanishing_point)
    #cv2.plot(vanishing_point)


    result = weighted_img(temp, image) # 원본 이미지에 검출된 선 overlap
    cv2.imshow('result',result) # 결과 이미지 출력
