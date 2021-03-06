"""drive source"""
import RPi.GPIO as GPIO
import time
import servo_motor as SERVO
import initial as INI
import arduinoserial as AS
import picam as PICAM
import servo_angle_calcul as SERVO_ANGLE

"""Setting"""
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

"""motor speed control"""
pwmA_motor = GPIO.PWM(pwmA_pin, 100)
pwmA_motor.start(0)
pwmB_motor = GPIO.PWM(pwmB_pin, 100)
pwmB_motor.start(0)
servo_motor = GPIO.PWM(servo_pwmpin, 50)
SERVO.servo_motor.start(4)
before_left=1
before_right=1
point = (0,0)
before_point = (240,0)
"""motor stop"""
def stop():
    pwmA_motor.ChangeDutyCycle(0)
    pwmB_motor.ChangeDutyCycle(0)    
"""forward moving"""
def forward():
    pwmA_motor.ChangeDutyCycle(75)
    GPIO.output(in1_pin,False)
    GPIO.output(in2_pin,True)
    pwmB_motor.ChangeDutyCycle(75) 
    GPIO.output(in3_pin,False)
    GPIO.output(in4_pin,True)

"""backward moving"""
def backward():
    pwmA_motor.ChangeDutyCycle(75) 
    GPIO.output(in1_pin,True)
    GPIO.output(in2_pin,False)
    pwmB_motor.ChangeDutyCycle(75)
    GPIO.output(in3_pin,True)
    GPIO.output(in4_pin,False)

"""main"""
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


    
