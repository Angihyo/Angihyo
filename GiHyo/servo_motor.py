"""servo_motor control"""
import RPi.GPIO as GPIO
import time
import initial as INI2

GPIO.setmode(GPIO.BCM)

servo_pwmpin = INI2.servo_pwm

GPIO.setup(servo_pwmpin, GPIO.OUT)

servo_motor = GPIO.PWM(servo_pwmpin, 50)

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
        servo_motor.ChangeDutyCycle(5.4)
    except KeyboardInterrupt:
       servo_motor.stop()
"""forward mode"""
def forward_Drive():
    try:
        servo_motor.ChangeDutyCycle(4)
    except KeyboardInterrupt:
       servo_motor.stop()

