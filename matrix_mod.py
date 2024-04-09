import time
import RPi.GPIO as GPIO
import LCD_mod as LCD

# Matrix_keyboard
R1 = 10
R2 = 9
R3 = 11
R4 = 5

C1 = 6
C2 = 13
C3 = 19

input_code = ""
attempts = 3

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

# Setting up matrix Keyboard
GPIO.setup(C1, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)
GPIO.setup(C2, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)
GPIO.setup(C3, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)

#Setting up Rows of Matrix Keypad as outputs
GPIO.setup(R1, GPIO.OUT)
GPIO.setup(R2, GPIO.OUT)
GPIO.setup(R3, GPIO.OUT)
GPIO.setup(R4, GPIO.OUT)

def check_reset(code):
    global input_code
    if code[-1] == '*':
        input_code = ""
        return True
    return False


def check_conf(code):
    global input_code
    if code[-1] == '#':
        input_code = ""
        return True
    return False
    

    
def readline(line, chars):
    global input_code
    GPIO.output(line, GPIO.HIGH)
    if GPIO.input(C1) == 1:
        input_code += chars[0]
        time.sleep(0.3)
    if GPIO.input(C2) == 1:
        input_code += chars[1]
        time.sleep(0.5)
    if GPIO.input(C3) == 1:
        input_code += chars[2]
        time.sleep(0.5)
    GPIO.output(line, GPIO.LOW)
    return input_code


def read_input(enroll_input_state):
    code = readline(R1, ["1", "2", "3"])
    code = readline(R2, ["4", "5", "6"])
    code = readline(R3, ["7", "8", "9"])
    code = readline(R4, ["*", "0", "#"])
    if '*' in code:
        if check_reset(code) == True:
            pass
            if enroll_input_state == "employer":
                LCD.lcd.clear()
                LCD.lcd.cursor_pos = (0, 0)
                LCD.lcd.write_string("Enter employer id")
                LCD.write_id(input_code, 1)
            if enroll_input_state == "sec_level":
                LCD.lcd.clear()
                LCD.lcd.cursor_pos = (0, 0)
                LCD.lcd.write_string("Enter security level")
                LCD.write_id(input_code, 1)
    if '#' in code:
        try:
            raise ValueError
        except ValueError:
            #TO DO - make revert to normal behavior
            print('ValueError')
    return input_code


def check_pass(security_code):
    code = readline(R1, ["1", "2", "3"])
    code = readline(R2, ["4", "5", "6"])
    code = readline(R3, ["7", "8", "9"])
    code = readline(R4, ["*", "0", "#"])
    LCD.write_input_code(code)
    global state
    state = "admin_mode"
    global attempts
    #passedFlag = "passed"
    if len(code) > 0:
        if check_reset(code) == True:
            LCD.mode_choosing(state) 
        elif check_conf(code) == True:
            if code == security_code:
                LCD.write_correct()
                time.sleep(2)
                LCD.hello_admin()
                return "passed"
            else:
                attempts -= 1
                LCD.write_incorrect()
                LCD.write_attempts(attempts)
                time.sleep(2)
                LCD.mode_choosing(state)
                if attempts == 0:
                    LCD.lcd.clear()
                    LCD.cursor_pos = (0, 0)
                    LCD.lcd.write_string("Attempts out!")
                    LCD.cursor_pos = (1,0)
                    LCD.lcd.write_string("Going to main menu..")
                    state = "choose_user_mode"
                    time.sleep(3)
                    attempts = 3 
                    LCD.hello_screen()
