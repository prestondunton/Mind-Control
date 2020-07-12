#! /usr/bin/python3

import serial
import pybrain
import time
import requests
import random

def main():

	gameTime = 10 # number of seconds the person is allowed to think for
	maxConcentration = 0


	''' # Use this code for live recording from the headset
	ser = serial.Serial("/dev/ttyS0", baudrate=9600, timeout=3.0)
	brain = pybrain.Brain(ser)
	'''

	# Use this code for reading from prerecorded brainwave data
	file = open("byte_stream.txt",'r')
	brain = pybrain.Brain(fileStream=file)


	print("\t")
	print("\t■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■")
	print("\t█                                                               █")
	print("\t█                   Colorado State University                   █")
	print("\t█                   CS 370  Operating Systems                   █")
	print("\t█        Term project for Andrew Fiel and Preston Dunton        █")
	print("\t█                        April 30, 2020                         █")
	print("\t█                                                               █")
	print("\t■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■")
	print("\t█                                                               █")
	print("\t█                ███╗   ███╗██╗███╗   ██╗██████╗                █") 
	print("\t█                ████╗ ████║██║████╗  ██║██╔══██╗               █")
	print("\t█                ██╔████╔██║██║██╔██╗ ██║██║  ██║               █")
	print("\t█                ██║╚██╔╝██║██║██║╚██╗██║██║  ██║               █")
	print("\t█                ██║ ╚═╝ ██║██║██║ ╚████║██████╔╝               █")
	print("\t█                ╚═╝     ╚═╝╚═╝╚═╝  ╚═══╝╚═════╝                █")
	print("\t█                                                               █")
	print("\t█  ██████╗ ██████╗ ███╗   ██╗████████╗██████╗  ██████╗ ██╗      █")
	print("\t█ ██╔════╝██╔═══██╗████╗  ██║╚══██╔══╝██╔══██╗██╔═══██╗██║      █")
	print("\t█ ██║     ██║   ██║██╔██╗ ██║   ██║   ██████╔╝██║   ██║██║      █")
	print("\t█ ██║     ██║   ██║██║╚██╗██║   ██║   ██╔══██╗██║   ██║██║      █")
	print("\t█ ╚██████╗╚██████╔╝██║ ╚████║   ██║   ██║  ██║╚██████╔╝███████╗ █")
	print("\t█  ╚═════╝ ╚═════╝ ╚═╝  ╚═══╝   ╚═╝   ╚═╝  ╚═╝ ╚═════╝ ╚══════╝ █")
	print("\t█                                                               █")
	print("\t■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■")
	time.sleep(5)
	print("\t█                                                               █")
	print("\t█        Get ready to post to Reddit with Mind Control!         █")
	print("\t█   You'll have %02d seconds to concentrate as hard as you can!   █" % gameTime)
	print("\t█                                                               █")
	print("\t■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■")
	time.sleep(3)
	print("\t█                                                               █")
	print("\t█                        Starting in 3!                         █")
	time.sleep(1)
	print("\t█                        Starting in 2!                         █")
	time.sleep(1)
	print("\t█                        Starting in 1!                         █")
	time.sleep(1)
	print("\t█                              GO!                              █")
	print("\t█                                                               █")
	print("\t■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■")
	print("\t█                                                               █")


	startTime = time.time()
	iteration = 0
	concentration = 0
	while(time.time() - startTime < gameTime):

		try:
			if(brain.update()):
				concentration = brain.readAttention()
		except EOFError:
			file.close()
			break

		if concentration > maxConcentration:
			maxConcentration = concentration

		if iteration % 40000 == 0:
			print("\t█      Concentration Level: %02d      Max Concentration: %02d       █" % (concentration,maxConcentration),end='\r',flush=True)

		iteration += 1

	print("\t█                          TIME'S UP!                           █")
	print("\t█                                                               █")
	print("\t■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■")

	requests.post("https://mind-control-csu.herokuapp.com/api/reddit",data=[("concentration",maxConcentration),("key",'''key removed for security reasons''')])

	print("\t█                                                               █")
	print("\t█              Your highest concentration was %02d!               █" % maxConcentration)
	print("\t█            Your post will have a max of %02d words!             █" % maxConcentration)
	print("\t█                                                               █")
	print("\t■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■")
	print("\t█                                                               █")
	print("\t█                Go check Reddit for your post!                 █")
	print("\t█       https://www.reddit.com/user/quality-content-bot/        █")
	print("\t█                                                               █")
	print("\t■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■")
	print("")

if __name__ == "__main__":
	main() 
