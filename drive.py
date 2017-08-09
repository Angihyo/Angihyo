import RPi.GPIO as GPIO
import time
import servo_motor as SERVO
import initial as INI

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

pwmA_pin = INI.pwmA
in1_pin = INI.in1
in2_pin = INI.in2
pwmB_pin = INI.pwmB
in3_pin = INI.in3
in4_pin = INI.in4

servo_pwmpin = INI.servo_pwm

left_sensor_pin = INI.left_sensor
right_sensor_pin = INI.right_sensor

GPIO.setup(pwmA_pin, GPIO.OUT)
GPIO.setup(in1_pin, GPIO.OUT)
GPIO.setup(in2_pin, GPIO.OUT)
GPIO.setup(pwmB_pin, GPIO.OUT)
GPIO.setup(in3_pin, GPIO.OUT)
GPIO.setup(in4_pin, GPIO.OUT)
GPIO.setup(servo_pwmpin, GPIO.OUT)
GPIO.setup(left_sensor_pin, GPIO.IN)
GPIO.setup(right_sensor_pin, GPIO.IN)

pwmA_motor = GPIO.PWM(pwmA_pin, 100)
pwmA_motor.start(0)
pwmB_motor = GPIO.PWM(pwmB_pin, 100)
pwmB_motor.start(0)
servo_motor = GPIO.PWM(servo_pwmpin, 50)
SERVO.servo_motor.start(4)
before_left=1
before_right=1
def stop():
    pwmA_motor.ChangeDutyCycle(0)
    pwmB_motor.ChangeDutyCycle(0)    

def forward():
    pwmA_motor.ChangeDutyCycle(75) 
    GPIO.output(in1_pin,True)
    GPIO.output(in2_pin,False)
    pwmB_motor.ChangeDutyCycle(75)
    GPIO.output(in3_pin,True)
    GPIO.output(in4_pin,False)

def backward():
    pwmA_motor.ChangeDutyCycle(75)
    GPIO.output(in1_pin,False)
    GPIO.output(in2_pin,True)
    pwmB_motor.ChangeDutyCycle(75) 
    GPIO.output(in3_pin,False)
    GPIO.output(in4_pin,True)
while True:
    left_input = GPIO.input(left_sensor_pin)
    right_input = GPIO.input(right_sensor_pin)
    if before_left != left_input or before_right != right_input:
        if left_input==0 and right_input==0:
            SERVO.forward_Drive()
            stop()
        elif left_input==0:
            SERVO.right_Drive()
        elif right_input==0:
            SERVO.left_Drive()
        else:
            SERVO.forward_Drive()
    forward()
    before_left = left_input
    before_right = right_input
    


    
