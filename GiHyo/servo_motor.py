"""servo_motor control"""
import RPi.GPIO as GPIO
import time
import initial as INI2

GPIO.setmode(GPIO.BCM)

servo_pwmpin = INI2.servo_pwm

GPIO.setup(servo_pwmpin, GPIO.OUT)

servo_motor = GPIO.PWM(servo_pwmpin, 50)
GPIO.setwarnings(False)

#3 ~ 5.4
"""left mode"""
def left_Drive():
    try:
        servo_motor.ChangeDutyCycle(3)
    except KeyboardInterrupt:
        servo_motor.stop()
"""right mode"""
def right_Drive():
    try:
        servo_motor.ChangeDutyCycle(5)
    except KeyboardInterrupt:
       servo_motor.stop()
"""forward mode"""
def forward_Drive():
    try:
        servo_motor.ChangeDutyCycle(4)
    except KeyboardInterrupt:
       servo_motor.stop()
"""exclusive servo control"""
def setting_Drive(servo_angle):
    try:
        if servo_angle==1:
            right_Drive()
            print("right")
        elif servo_angle==-1:
            left_Drive()
            print("left")
        else:
            servo_motor.ChangeDutyCycle(4+servo_angle)
            print("angle")
            print(4+servo_angle)
    except KeyboardInterrupt:
        servo_motor.stop()
