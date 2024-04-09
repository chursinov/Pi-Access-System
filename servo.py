import RPi.GPIO as GPIO
import time

RELAY = 20

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(RELAY,GPIO.OUT)
GPIO.output(RELAY, GPIO.HIGH)

def open_lock():
    GPIO.output(RELAY, GPIO.LOW)
    time.sleep(3)
    GPIO.output(RELAY, GPIO.HIGH)