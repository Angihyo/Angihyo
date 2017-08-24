import serial

port = "/dev/ttyUSB0"
serialFromArduino = serial.Serial(port, 9600)
serialFromArduino.flushInput()

while True:
    if(serialFromArduino.inWaiting() >0):
        input_s =serialFromArduino.readline()
        input = int(input_s)
        print(input)
