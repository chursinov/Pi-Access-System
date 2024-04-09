# import RPi.GPIO as GPIO

# GPIO.setmode(GPIO.BOARD)
# GPIO.setwarnings(False)

# LED = 7

# GPIO.setup(LED, GPIO.OUT)

# state = GPIO.input(LED)

# if state:
#     GPIO.output(LED, GPIO.LOW)
# else:
#     GPIO.output(LED, GPIO.HIGH)
import RPi.GPIO as IO
import time

IO.setwarnings(False)
IO.setmode(IO.BCM)
IO.setup(19,IO.OUT)
IO.setup(26,IO.IN)

IO.setup(13,IO.IN)
IO.setup(6,IO.OUT)

led_state_green= False
led_state_red = False
led_state = ""

IO.output(6, False)
while 1:
    #Turning to Green Light
    if IO.input(13) == False and (led_state == "Red" or led_state == ""):
        IO.output(19, False)
        IO.output(6, True)
        led_state = "Green"
        time.sleep(0.5)
    #Turning to Red Light
    elif IO.input(26) == False and (led_state == "Green" or led_state == ""):
        IO.output(6, False)
        IO.output(19, True)
        led_state = "Red"
        time.sleep(0.5)

