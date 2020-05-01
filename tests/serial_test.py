import serial

ser = serial.Serial("/dev/ttyS0", baudrate=9600, timeout=3.0) #setup the serial port with the settings

print("Trying to read serial port")

while True:
    x = ser.read()
    print(x)
