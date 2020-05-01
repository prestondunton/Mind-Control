import serial
import pybrain

ser = serial.Serial("/dev/ttyS0", baudrate=9600, timeout=3.0)

brain = pybrain.Brain(brainStream=ser,debug=True)

print("Trying to use my brain!")

while(True):
	
	if(brain.update()):
		print("Errors:",brain.readErrors())
		print("Brainwave Data:",brain.readCSV())
		print("Attention:",brain.readAttention())
		brain.clearErrors()
