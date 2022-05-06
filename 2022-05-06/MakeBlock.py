from megapi import *
import time
import pygame
import RPi.GPIO as GPIO

announce = time.time()
distance = 123

# -=Function=-
def Forward(port, speed):
	sleep(0.4)
	bot.encoderMotorRun(port,speed)

def Backward(port, speed):
	bot.encoderMotorRun(port, speed)

# -=UltrasonicSensor=-
def UltraSonic(port):
	global distance
	distance = port
	print(distance)

# -=SoundPlay=-
def SoundPlay(SoundFile):
	SoundList = ["Ms C.mp3", "Mr Williams.mp3"] # Ms. C = 0 | Mr. W = 1
	pygame.mixer.init()
	pygame.mixer.music.set_volume(0.2) # Volume: (0 - 1)
	pygame.mixer.music.load(SoundList[SoundFile])
	pygame.mixer.music.play()
	while pygame.mixer.music.get_busy() == True:
		continue

# -=GPIO=-
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)

	# Speaker
speaker_buttonPin1 = 32
speaker_buttonPin2 = 22
GPIO.setup(speaker_buttonPin1, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(speaker_buttonPin2, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

    # Sound Sensor
sound_sensorPin = 18
GPIO.setup(sound_sensorPin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

# -=Main=-
if __name__ == '__main__':
	bot = MegaPi()
	bot.start()
	output = 0

	while True:
		# -=SET UP=-
		if GPIO.input(speaker_buttonPin1) == GPIO.HIGH:
			output = 1
		
		elif GPIO.input(speaker_buttonPin2) == GPIO.HIGH:
			output = 2
		
		else:
			pass

		# -=GO OUT=-
		if output == 1:
			
			# Sound
			print(f"Time: {announce}")
			if time.time() - announce > 10:
				announce = time.time()
				SoundPlay(0)
#			SoundPlay(0)
				
			# Ultra Sonic
			bot.ultrasonicSensorRead(6,UltraSonic)
			
			# Movement
			if distance < 8:
				print(f"Smaller distance: {distance}")
				Forward(4,-50)
				Backward(1, 0)
			else:
				Forward(4, -50) # Left Wheel -25
                Backward(4,-50)
				Backward(1, 50) # Right Wheel 25

		# -=BE QUIET=-
		elif output == 2:
			if GPIO.input(sound_sensorPin) == GPIO.HIGH:
				SoundPlay(1)
		
		else:
			pass
	
