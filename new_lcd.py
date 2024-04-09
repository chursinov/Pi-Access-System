import LCD_mod as LCD
import RPi.GPIO as GPIO
import time
from pad4pi import rpi_gpio

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

LCD.hello_screen()