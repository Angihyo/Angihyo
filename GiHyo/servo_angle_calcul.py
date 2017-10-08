import math

def Servo_angle_calcul(vanishingpoint):
    height = 360 - vanishingpoint[1]
    width = vanishingpoint[0] - 240
    angle = 180*(width/height) / math.pi
    print(angle)
    if angle > 30:
        return 1  #turn right maximum
    elif angle < -30:
        return -1 #turn left maximum
    else:
        return angle/30
