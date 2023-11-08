
import time
from rpi_ws281x import *
import argparse,random

# LED strip configuration:
LED_COUNT      = 75     # Number of LED pixels.
LED_PIN        = 13      # GPIO pin connected to the pixels (18 uses PWM!).
#LED_PIN        = 10      # GPIO pin connected to the pixels (10 uses SPI /dev/spidev0.0).
LED_FREQ_HZ    = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA        = 10      # DMA channel to use for generating a signal (try 10)
LED_BRIGHTNESS = 255      # Set to 0 for darkest and 255 for brightest
LED_INVERT     = False   # True to invert the signal (when using NPN transistor level shift)
LED_CHANNEL    = 1       # set to '1' for GPIOs 13, 19, 41, 45 or 53



# Define functions which animate LEDs in various ways.
def colorWipe(strip, color, wait_ms=50):
    """Wipe color across display a pixel at a time."""
    for i in range(strip.numPixels()):
        strip.setPixelColor(i, color)
        strip.show()
        time.sleep(wait_ms/1000.0)

def theaterChase(strip, color, wait_ms=50, iterations=10):
    """Movie theater light style chaser animation."""
    for j in range(iterations):
        for q in range(3):
            for i in range(0, strip.numPixels(), 3):
                strip.setPixelColor(i+q, color)
            strip.show()
            time.sleep(wait_ms/1000.0)
            for i in range(0, strip.numPixels(), 3):
                strip.setPixelColor(i+q, 0)

def wheel(pos):
    """Generate rainbow colors across 0-255 positions."""
    if pos < 85:
        return Color(pos * 3, 255 - pos * 3, 0)
    elif pos < 170:
        pos -= 85
        return Color(255 - pos * 3, 0, pos * 3)
    else:
        pos -= 170
        return Color(0, pos * 3, 255 - pos * 3)

def rainbow(strip, wait_ms=20, iterations=1):
    """Draw rainbow that fades across all pixels at once."""
    for j in range(256*iterations):
        for i in range(strip.numPixels()):
            strip.setPixelColor(i, wheel((i+j) & 255))
        strip.show()
        time.sleep(wait_ms/1000.0)

def rainbowCycle(strip, wait_ms=20, iterations=5):
    """Draw rainbow that uniformly distributes itself across all pixels."""
    for j in range(256*iterations):
        for i in range(strip.numPixels()):
            strip.setPixelColor(i, wheel((int(i * 256 / strip.numPixels()) + j) & 255))
        strip.show()
        time.sleep(wait_ms/1000.0)

def theaterChaseRainbow(strip, wait_ms=50):
    """Rainbow movie theater light style chaser animation."""
    for j in range(256):
        for q in range(3):
            for i in range(0, strip.numPixels(), 3):
                strip.setPixelColor(i+q, wheel((i+j) % 255))
            strip.show()
            time.sleep(wait_ms/1000.0)
            for i in range(0, strip.numPixels(), 3):
                strip.setPixelColor(i+q, 0)

def blinkLightsBlue(strip):
    colors = [Color(15, 3, 252),Color(3, 126, 202),Color(15, 232, 252)]
    for i in range(0,strip.numPixels()):
        strip.setPixelColor(i,colors[random.randint(0,2)])
    strip.show()
    
def blinkLightsOrange(strip):
    colors = [Color(252, 169, 3),Color(252, 236, 3)]
    for i in range(0,strip.numPixels()):
        strip.setPixelColor(i,colors[random.randint(0,1)])
    strip.show()
        

def snowflake(strip):
        colors = [Color(15, 3, 252),Color(3, 126, 202),Color(15, 232, 252)]
        for i in range(0,27):
            strip.setPixelColor(i,Color(15, 3, 252))
        strip.show()
        
def spell(strip,wait):
    """ice spell"""
    for i in range(0, strip.numPixels()):
        ball(strip,i)                
        time.sleep(wait/1000.0)
    colorWipe(strip,Color(0,0,0),0)

def ball(strip,pos):
    for i in range(0,pos):
        strip.setPixelColor(i,Color(0,0,0))
    strip.setPixelColor(pos+0,Color(1, 13, 17))
    strip.setPixelColor(pos+1,Color(2, 32, 47))
    strip.setPixelColor(pos+2,Color(2, 52, 77))
    strip.setPixelColor(pos+3,Color(3, 82, 127))
    strip.setPixelColor(pos+4,Color(3, 186, 252))
    strip.setPixelColor(pos+5,Color(3, 186, 252))
    
    strip.show()



# Main program logic follows:
if __name__ == '__main__':
    # Process arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--clear', action='store_true', help='clear the display on exit')
    args = parser.parse_args()

    # Create NeoPixel object with appropriate configuration.
    strip_test = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL)
    # Intialize the library (must be called once before other functions).
    strip_test.begin()

    print ('Press Ctrl-C to quit.')
    if not args.clear:
        print('Use "-c" argument to clear LEDs on exit')

    try:
        while True:
            print ('Color wipe animations.')
            #colorWipe(strip, Color(15, 3, 252),0) # Red wipe
            #time.sleep(5)
            #colorWipe(strip, Color(15, 232, 252),0)  # Blue wipe
            #time.sleep(5)
            #colorWipe(strip, Color(3, 186, 252),0)  # Green wipe
            #time.sleep(5)
            #colorWipe(strip, Color(252, 169, 3),0)  # Green wipe
            #colorWipe(strip, Color(252, 236, 3),0)  # Green wipe
            #time.sleep(5)
            #blinkLightsBlue(strip_test)
            #theaterChaseorange(strip)
            blinkLightsBlue(strip_test)
            #time.sleep(250/1000.0)
            #spell(strip_test,55)    
            time.sleep(155/1000.0)

    except KeyboardInterrupt:
        if args.clear:
            colorWipe(strip_test, Color(0,0,0), 0)

    if args.clear:
            colorWipe(strip_test, Color(0,0,0), 0)