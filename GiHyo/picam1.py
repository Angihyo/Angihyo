
from picamera.array import PiRGBArray
from picamera import PiCamera
import time
import cv2
import finallevel1

camera = PiCamera()
camera.resolution = (480, 320)
camera.framerate = 32
rawCapture = PiRGBArray(camera, size=(480,320))

time.sleep(0.1)

for frame in camera.capture_continuous(rawCapture, format='bgr', use_video_port= True):
    image = frame.array
    try:
        finallevel1.LineDetecting(image)
    except:
        pass
    cv2.imshow('Frame', image)
    while True:
        try:
            point = PICAM.camera_operating(before_point)
            print(point)
        except:
            point = before_point
        before_point = point
        left_input = GPIO.input(left_sensor_pin)
        right_input = GPIO.input(right_sensor_pin)
        #middle_input = AS.serial_control()
        middle_input = 30
        print(left_input)
        print(right_input)
        if middle_input > 20:
            forward()
            if before_left == left_input or before_right == right_input:
                if left_input==0 and right_input==0:
                    SERVO.forward_Drive()
                    #stop()
                    print('forward')
                elif left_input==0:
                    SERVO.right_Drive()
                    print('right')
                elif right_input==0:
                    SERVO.left_Drive()
                    print('left')
                else:
                    SERVO.setting_Drive(SERVO_ANGLE.Servo_angle_calcul(point))
        else:
            stop()
        before_left = left_input
        before_right = right_input

    key = cv2.waitKey(1)&0xff
    rawCapture.truncate(0)
    if key == 27:
        break

rawCapture.release()
cv2.destroyAllWindows()
 
