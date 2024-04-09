import RPi.GPIO as GPIO
from pyfingerprint.pyfingerprint import PyFingerprint
import time

#Buttons
ENROLL = 26
SEARCH = 19
CLR = 13
DECR = 6

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

#Setting up buttons as ins
GPIO.setup(ENROLL, GPIO.IN)
GPIO.setup(SEARCH, GPIO.IN)
GPIO.setup(CLR, GPIO.IN)
GPIO.setup(DECR, GPIO.IN)

global fingerprint
fingerprint = []

def enrollFinger():
    print('Enrolling finger')
    time.sleep(1)
    print('Waiting for finger')
    time.sleep(1)
    print('Place finger')
    while (f.readImage() == False):
        pass
    f.convertImage(0x01)
    result = f.searchTemplate()
    positionNumber = result[0]
    print(positionNumber)
    if positionNumber >= 0:
        print('Error! Finger already exists')
        print('Exiting...Try again')
        return
    print('Remove finger')
    time.sleep(1)
    print('Place the same finger again')
    while f.readImage() == False:
        pass
    f.convertImage(0x02)
    if f.compareCharacteristics() == 0:
        print('Finger do not match')
        print('Try Again!')
        return
    f.createTemplate()
    positionNumber = f.storeTemplate()
    specs = f.downloadCharacteristics()
    print('Finger Enrolled Succesfully')
    print('Stored at pos: ', positionNumber)
    return specs

def search_finger(fingerprint):
    try:
        print('Waiting for finger')
        #while f.readImage() == False:
            #time.sleep(0.5)
        f.uploadCharacteristics(characteristicsData=fingerprint)
        result = f.searchTemplate()
        positionNumber = result[0]
        accuracy_score = result[1]
        print(accuracy_score)
        if positionNumber == -1:
            print('Access if prohibited')
            time.sleep(1)
            return
        else:
            print('Found Template at pos: ', positionNumber)
    except Exception as e:
        print('Operation Failed!')
        print('Exception message: ', str(e))

try:
    f = PyFingerprint('/dev/ttyS0', 57600, 0xFFFFFFFF, 0x00000000)
    print('Fingerprint sensor initiated')
    if (f.verifyPassword() == False):
        raise ValueError('The given fingerprint password is wrong')
    
except Exception as e:
    print('Exception message: ' + str(e))

while True:
    if GPIO.input(ENROLL) == False:
        print('test')
        fingerprint = enrollFinger()
    
    if GPIO.input(SEARCH) == False:
        print('Scanning...')
        search_finger(fingerprint)
    if GPIO.input(CLR) == False:
        f.clearDatabase()
        print('Database cleared')
