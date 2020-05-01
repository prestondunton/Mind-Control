import pybrain

file = open("byte_stream.txt", 'r')

brain = pybrain.Brain(fileStream=file,debug=False)

print("Reading file")

while(True):
	try:
		if(brain.update()):
			print("Errors:",brain.readErrors())
			print("Brainwave Data:",brain.readCSV())
			print("Attention:",brain.readAttention())
			brain.clearErrors()
	except EOFError:
		print("Done reading file")
		file.close()
		break

