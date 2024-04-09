import RPi.GPIO as IO
import time

#Buzzer pin
BUZZER = 18

# IO.setwarnings(False)
# IO.setmode(IO.BCM)
# IO.setup(Buzzer, IO.OUT)
# time.sleep(0.05)
# IO.setup(Buzzer, IO.IN)
# time.sleep(2)
# IO.setup(Buzzer, IO.OUT)
# time.sleep(0.6)
# IO.setup(Buzzer, IO.IN)

IO.setwarnings(False)
IO.setmode(IO.BCM)
IO.setup(BUZZER, IO.OUT)
#IO.output(Buzzer, IO.HIGH)





def on():
    IO.output(BUZZER, IO.LOW)


def off():
    IO.output(BUZZER, IO.HIGH)

def correct_beep():
    on()
    time.sleep(0.2)
    off()
    time.sleep(0.15)
    on()
    time.sleep(0.6)
    off()

def incorrect_beep():
    on()
    time.sleep(0.3)
    off()
    time.sleep(0.2)
    on()
    time.sleep(0.3)
    off()
    time.sleep(0.2)
    on()
    time.sleep(0.3)
    off()

def beep():
    on()
    time.sleep(0.2)
    off()
    