import serial
"""serialcontrol"""
def serial_control():
    port = "/dev/ttyUSB0"
    serialFromArduino = serial.Serial(port, 115200)
    serialFromArduino.flushInput()
    """arduino_data read"""
    while True:
        if(serialFromArduino.inWaiting() >0):
            input_s =serialFromArduino.readline()
            input = int(input_s)
            print(input)
            return input
