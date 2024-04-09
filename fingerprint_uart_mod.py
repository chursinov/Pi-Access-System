import RPi.GPIO as GPIO
from pyfingerprint.pyfingerprint import PyFingerprint
import time
import DB_mod as DB
import matrix_mod as matrix
import LCD_mod as LCD


def enrollFinger(CONFIRM_BUTTON):
    global state
    while (f.readImage() == False):
        pass
    f.convertImage(0x01)
    LCD.lcd.cursor_pos = (2, 0)
    LCD.lcd.write_string("Remove Finger")
    time.sleep(1)
    LCD.lcd.cursor_pos(3, 0)
    LCD.lcd.write_string("Place same finger")
    while f.readImage() == False:
        pass
    f.convertImage(0x02)
    if f.compareCharacteristics() == 0:
        LCD.lcd.clear()
        LCD.lcd.cursor_pos = (0,0)
        LCD.lcd.write_string("Finger not found")
        LCD.lcd.cursor_pos = (1,0)
        LCD.lcd.write_string("Try Again")
        time.sleep()
        state = "choose_admin_action"
        LCD.hello_admin()
        return
    f.createTemplate()
    specs = f.downloadCharacteristics()
    if DB.fetchFingers() != False:
        specs_DB_tuple = DB.fetchFingers()
        for i in range(len(specs_DB_tuple)):
            specs_DB = specs_DB_tuple[i][0]
            f.uploadCharacteristics(1, specs_DB)
            if f.compareCharacteristics() != 0:
                LCD.lcd.clear()
                LCD.lcd.cursor_pos = (0,0)
                LCD.lcd.write_string("Error!")
                LCD.lcd.cursor_pos = (1,0)
                LCD.lcd.write_string("Fingerprint exists")
                time.sleep(2)
                state = "choose_admin_action"
                LCD.hello_admin()
                return
    #positionNumber = f.storeTemplate()
    #specs = f.downloadCharacteristics()
    LCD.lcd.clear()
    LCD.lcd.cursor_pos = (0,0)
    LCD.lcd.write_string("Enter employer id")
    matrix.input_code = ""
    while True:
        enroll_input_state = "employer"
        if GPIO.input(CONFIRM_BUTTON) == False:
            break
        emp_id = matrix.read_input(enroll_input_state)
        LCD.write_id(matrix.input_code,1)
    LCD.enter_emp_id_msg(emp_id)
    LCD.lcd.cursor_pos = (2,0)
    LCD.lcd.write_string("Confirmed!")
    time.sleep(3)
    LCD.lcd.clear()
    LCD.lcd.cursor_pos = (0,0)
    LCD.lcd.write_string("Enter sec. level")
    matrix.input_code = ""
    while True:
        enroll_input_state = "sec_level"
        if GPIO.input(CONFIRM_BUTTON) == False:
            break
        sec_level = matrix.read_input(enroll_input_state)
        LCD.write_id(matrix.input_code,1)
    LCD.enter_sec_level_msg(sec_level)
    LCD.lcd.cursor_pos = (2,0)
    LCD.lcd.write_string("Confirmed!")
    time.sleep(0.5)
    while True:
        if GPIO.input(CONFIRM_BUTTON) == False:
            if DB.addFingerPrint(specs,emp_id,sec_level) == True:
                LCD.lcd.clear()
                LCD.lcd.cursor_pos = (0,0)
                LCD.lcd.write_string("Commited to DB!")
                time.sleep(3)
                break
            else:
                LCD.lcd.clear()
                LCD.lcd.cursor_pos = (0,0)
                LCD.lcd.write_string("Error!")
                LCD.lcd.cursor_pos = (1,0)
                LCD.lcd.write_string("Cant add more than one fingerprint per user")
                time.sleep(3)
                break
    state = "choose_admin_action"
    LCD.hello_admin()

    
def search_finger():
    while f.readImage() == False:
        pass
    f.convertImage(0x02)
    if DB.fetchFingersEmployersSecLevels() != None:
        specs_DB_tuple = DB.fetchFingersEmployersSecLevels()
        for i in range(len(specs_DB_tuple)):
            specs_DB, name, surname, sec_level = specs_DB_tuple[i]
            f.uploadCharacteristics(1, specs_DB)
            if f.compareCharacteristics() != 0:
                return (name, surname, sec_level)
            else:
                continue
        return False

try:
    f = PyFingerprint('/dev/ttyS0', 57600, 0xFFFFFFFF, 0x00000000)
    #print('Fingerprint sensor initiated')
    if (f.verifyPassword() == False):
        raise ValueError('The given fingerprint password is wrong')
    
except Exception as e:
    print('Exception message: ' + str(e))