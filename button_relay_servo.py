import RPi.GPIO as GPIO
import time

BUTTON = 4
RELAY = 17

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(BUTTON,GPIO.IN)
GPIO.setup(RELAY,GPIO.OUT)
GPIO.output(RELAY, GPIO.HIGH)

while True:
    if GPIO.input(BUTTON) == GPIO.LOW:
        GPIO.output(RELAY, GPIO.LOW)
        time.sleep(3)
        GPIO.output(RELAY, GPIO.HIGH)