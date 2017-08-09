import RPi.GPIO as GPIO
import time
import initial as INI2

GPIO.setmode(GPIO.BCM)

servo_pwmpin = INI2.servo_pwm

GPIO.setup(servo_pwmpin, GPIO.OUT)

servo_motor = GPIO.PWM(servo_pwmpin, 50)

#3 ~ 5.4

def left_Drive():
    try:
        servo_motor.ChangeDutyCycle(3)
    except KeyboardInterrupt:
        servo_motor.stop()
def right_Drive():
    try:
        servo_motor.ChangeDutyCycle(5.4)
    except KeyboardInterrupt:
       servo_motor.stop()
def forward_Drive():
    try:
        servo_motor.ChangeDutyCycle(4)
    except KeyboardInterrupt:
       servo_motor.stop()

