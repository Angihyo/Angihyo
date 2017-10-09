from picamera.array import PiRGBArray
from picamera import PiCamera
import time
import cv2
import finallevel1
import gogo

def camera_operating(before_point):
    cap = cv2.VideoCaptere(0)
    cap.set(3.480)
    cap.set(4.320)
    okdk = cap.isOpened()
    print(okdk)
    vanish_point = before_point
    #camera = PiCamera()
    #camera.resolution = (480, 320)
    #camera.framerate = 32
    #camera.capture('camera.jpg', format = 'bgr', use_video_port=True)
    ret,frame = cap.read()
    #time.sleep(0.1)
    #point = 0
    image = frame
    try:
        #point = finallevel1.LineDetecting(image)
        vanish_point = gogo.detect_lanes_img(image)
        print(vanish_point)
    except:
        pass
    #cv2.imshow('frame', image)
    cap.release()
    cv2.destroyAllWindows()
    #if key == 27:
    #if point is None:
    return vanish_point
