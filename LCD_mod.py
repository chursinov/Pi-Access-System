from RPLCD import *
import time
from RPLCD.i2c import CharLCD

lcd = CharLCD('PCF8574', 0x27)

def hello_screen(lcd=lcd):
    lcd.clear()
    lcd.cursor_pos = (0,0)
    lcd.write_string('Welcome to SKUD')
    lcd.cursor_pos = (1,0)
    lcd.write_string('Input user mode')
    lcd.cursor_pos = (2, 0)
    lcd.write_string('1 - Admin mode')
    lcd.cursor_pos = (3, 0)
    lcd.write_string('2 - User mode')

def mode_choosing(chosen_mode):
    match chosen_mode:
        case "admin_mode":
            lcd.clear()
            lcd.cursor_pos = (0, 0)
            lcd.write_string('Enter pin!')
        case "user_mode":
            lcd.clear()
            lcd.cursor_pos = (0, 0)
            lcd.write_string('User mode')
            lcd.cursor_pos = (1, 0)
            lcd.write_string('Place Finger')

def write_correct():
    lcd.cursor_pos = (2, 0)
    lcd.write_string("Correct")

def write_incorrect():
    lcd.cursor_pos = (2, 0)
    lcd.write_string("Incorrect")

def write_attempts(attempts):
    lcd.cursor_pos = (3,0)
    lcd.write_string(f"Attempts left - {attempts}")

def write_input_code(code):
    to_replace = code[0:-1]
    replaced = code.replace(to_replace, '*'*len(to_replace))
    lcd.cursor_pos = (1,0)
    lcd.write_string(replaced)

def write_id(code, pos):
    lcd.cursor_pos = (pos,0)
    lcd.write_string(f"You entered: {code}")

def write_access_mode(value):
    lcd.clear()
    lcd.write_string(f'{value} level has set')

def hello_admin():
    lcd.clear()
    lcd.cursor_pos = (0,0)
    lcd.write_string('Hello, Admin')
    lcd.cursor_pos = (1,0)
    lcd.write_string('Choose action:')
    lcd.cursor_pos = (2,0)
    lcd.write_string('1 - to add finger')
    lcd.cursor_pos = (3,0)
    lcd.write_string('2 - to delete finger')

def enter_emp_id_msg(emp_id):
    lcd.cursor_pos = (1,0)
    lcd.write_string(f"Employer {emp_id} linked")

def enter_sec_level_msg(sec_level):
    lcd.cursor_pos = (1,0)
    lcd.write_string(f"Level {sec_level} has set") 

