'''
	Raspberry Pi GPIO Status and Control
'''
import RPi.GPIO as GPIO
from flask import Flask, render_template, request
import threading
import time
from rpi_ws281x import *
import random

# LED strip configuration:
LED_COUNT      = 77     # Number of LED pixels.
LED_FREQ_HZ    = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA        = 10      # DMA channel to use for generating a signal (try 10)
LED_BRIGHTNESS = 255      # Set to 0 for darkest and 255 for brightest
LED_INVERT     = False   # True to invert the signal (when using NPN transistor level shift)

app = Flask(__name__)
	

@app.route("/")
def index():
	return update()

# Define functions which animate LEDs in various ways.
def colorWipe(strip, color, wait_ms=50):
	"""Wipe color across display a pixel at a time."""
	for i in range(strip.numPixels()):
		strip.setPixelColor(i, color)
	strip.show()
		
def spell(strip,wait):
	"""ice spell"""
	print("fire spell")
	restartstair=False
	if stairEvent.is_set():
		stairEvent.clear()
		restartstair=True

	for i in range(0, strip.numPixels()-1):
		ball(strip,i)                
		time.sleep(wait/1000.0)
	strip.setPixelColor(73,Color(3, 186, 252))
	strip.setPixelColor(74,Color(3, 186, 252))
	strip.show()
	for i in range(250,0,-25):
		strip.setBrightness(i)
		strip.show()
		time.sleep(wait/1000.0)
	colorWipe(strip,Color(0,0,0),0)
	if restartstair:
		stairEvent.set()

def ball(strip,pos):
	for i in range(0,pos):
		strip.setPixelColor(i,Color(0,0,0))
	colors = [Color(1, 13, 17),Color(2, 32, 47),Color(2, 52, 77),Color(3, 82, 127),Color(3, 82, 127),Color(3, 186, 252),Color(3, 186, 252)]
	for i in range(0,6):
		strip.setPixelColor(pos+i,colors[i] if pos+i<74 else colors[5])
		#print(pos+i,colors[i] if pos+i<74 else colors[5])
	strip.show()

def threadStair(event,strip1,strip2,eventStop):
	try:
		while event.wait():
			if eventStop.is_set():
				colorWipe(strip1,0,0)
				colorWipe(strip2,0,0)
				return
			if stairscolor==1:
				blinkLightsOrange(strip1)
				blinkLightsOrange(strip2)
			elif stairscolor==0:
				blinkLightsBlue(strip1)
				blinkLightsBlue(strip2)
			time.sleep(150/1000.0)
			if not event.is_set():
				colorWipe(strip1,0,0)
				colorWipe(strip2,0,0)
	except:
		colorWipe(strip1,0,0)
		colorWipe(strip2,0,0)

		return

def blinkLightsBlue(strip):
	colors = [Color(15, 3, 252),Color(3, 126, 202),Color(15, 232, 252)]
	for i in range(0,strip.numPixels()):
		strip.setPixelColor(i,colors[random.randint(0,2)])
	strip.show()
	
def blinkLightsOrange(strip):
	colors = [Color(252,169,3),Color(252,236,3)]
	for i in range(0,strip.numPixels()):
		strip.setPixelColor(i,colors[random.randint(0,1)])
	strip.show()

def snowflake(strip):
	for i in range(0,strip.numPixels()):
		strip.setPixelColor(i,Color(3, 126, 202))
	strip.show()

@app.route("/<deviceName>/<action>")
def action(deviceName, action):
	global flakeSts,backcolor,backSts,stairsSts,stairscolor
	if deviceName == 'stairs':
		if action == 'on':
			stairsSts = 1
		
		elif action == 'off':
			stairsSts = 0
	

	if deviceName == 'flake':
		if action == 'on':
			flakeSts = 1
		
		elif action == 'off':
			flakeSts = 0
	
	if deviceName == 'spell' and action == "fire":
		spell(strip_back,10)
		colorWipe(strip_back, Color(0,0,0), 0)
		return update()
	
	if deviceName == 'back':
		if action == 'on':
			backSts = 1
		
		elif action == 'off':
			backSts = 0
	
	if deviceName == 'staircolor':
		if action == "orange":
			stairscolor = 1
		elif action == 'blue':
			stairscolor = 0

	
	elif deviceName == "stairs":
		if action == "off":
			print("stairs off")
			stairEvent.clear()

		elif action == "on":
			print("stairs on")
			stairEvent.set()

	elif deviceName == 'flake':
		if action == "off":
			print('flake off')
			colorWipe(strip_flake,0,0)

		elif action == "on":
			print('flake on blue')
			snowflake(strip_flake)
			
	return update()

def update():
	global flakeSts,stairsSts,stairscolor
	
	templateData = {
	  		'stairs'  : stairsSts,
	  		'flake'  : flakeSts,
			'staircolor' : stairscolor
	}
	return render_template('index.html', **templateData)

if __name__ == "__main__":
	
	stairsSts = 0
	flakeSts = 0
	stairscolor = 0	
	LED_GPIO        = 13 
	LED_CHANNEL    = 1
	LED_COUNT      = 75   
	strip_back = Adafruit_NeoPixel(LED_COUNT, LED_GPIO, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL)
	# Intialize the library (must be called once before other functions).
	strip_back.begin()
	
	LED_GPIO        = 12      # GPIO pin connected to the pixels (18 uses PWM!).
	LED_CHANNEL    = 0
	strip_side = Adafruit_NeoPixel(LED_COUNT, LED_GPIO, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL)
	# Intialize the library (must be called once before other functions).
	strip_side.begin()
	
	LED_GPIO        = 21      # GPIO pin connected to the pixels (18 uses PWM!).
	LED_CHANNEL    = 0
	LED_COUNT      = 31
	strip_flake = Adafruit_NeoPixel(LED_COUNT, LED_GPIO, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL)
	# Intialize the library (must be called once before other functions).
	strip_flake.begin()
	# spell(strip,5)
	stopEvent= threading.Event()
	stopEvent.clear()
	stairEvent = threading.Event()
	stairEvent.clear()
	stairThread = threading.Thread(target=threadStair,args=(stairEvent,strip_side,strip_back,stopEvent,))
	stairThread.start()
	try:
		app.run(host='0.0.0.0', port=80, debug=False)
	except:
		print("caught")
		stopEvent.set()
		stairEvent.set()
		stairThread.join()