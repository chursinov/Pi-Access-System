import RPi.GPIO as GPIO
import time

# GPIO.setmode(GPIO.BOARD)
# GPIO.setwarnings(False)

RED_LED = 23
GREEN_LED = 8


GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(RED_LED,GPIO.OUT)
GPIO.setup(GREEN_LED,GPIO.OUT)

def blink_red():
    GPIO.output(RED_LED, GPIO.HIGH)
    time.sleep(1)
    GPIO.output(RED_LED, GPIO.LOW)

def blink_green():
    GPIO.output(GREEN_LED, GPIO.HIGH)
    time.sleep(1)
    GPIO.output(GREEN_LED, GPIO.LOW)

        

