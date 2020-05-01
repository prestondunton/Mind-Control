import serial
import pybrain

ser = serial.Serial("/dev/ttyS0", baudrate=9600, timeout=3.0)

brain = pybrain.Brain(ser,debug=True)

packet = [2, 200, 131, 24, 26, 142, 216, 26, 172, 145, 9, 158, 11, 6, 168, 227, 1, 247, 134, 2, 108, 63, 0, 180, 225, 0, 49, 171, 4, 0, 5, 0]

print(len(packet))

brain.packetLength = len(packet)
brain.packetData = packet

brain.parsePacket()
print(brain.readCSV())

