import LCD_mod as LCD
import matrix_mod as matrix
import RPi.GPIO as GPIO
import time
from pad4pi import rpi_gpio
import fingerprint_uart_mod as fingerprint
import buzzer as buzzer
import LED as LED
import servo as servo
import DB_mod as DB
import socket
import logging_mod as Log

# Buttons
ADMIN_BUTTON = 4
USER_BUTTON = 17
HOME_BUTTON = 27
CONFIRM_BUTTON = 22

#Variable to store input pin and secret code to compare
security_code = "1598#"
passed = False

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)


# Setting up buttons
GPIO.setup(ADMIN_BUTTON, GPIO.IN)
GPIO.setup(USER_BUTTON, GPIO.IN)
GPIO.setup(HOME_BUTTON, GPIO.IN)
GPIO.setup(CONFIRM_BUTTON, GPIO.IN)

#Setting up LCD
LCD.hello_screen()

access_levels = ['1', '2', '3', '4']

state = "choose_user_mode"
#Buzzer off
buzzer.off()
while True:
    # Main menu
    if GPIO.input(ADMIN_BUTTON) == False:
        # Go to to admin mode
        buzzer.beep()
        time.sleep(0.5)
        state = "admin_mode"
        LCD.mode_choosing(state)
    if GPIO.input(USER_BUTTON) == False:
        # Go to user mode
        buzzer.beep()
        state = "user_mode"
        time.sleep(0.5)
        LCD.mode_choosing(state)
    if GPIO.input(HOME_BUTTON) == False:
        # Go back to main menu
        buzzer.beep()
        state = "mode_choosing"
        time.sleep(0.5)
        LCD.lcd.clear()
        LCD.hello_screen()
    if GPIO.input(CONFIRM_BUTTON) == False:
        # Confirm action
        buzzer.beep()
        time.sleep(0.5)
    
    
    if state == "admin_mode":
        if matrix.check_pass(security_code) == "passed":
            state = "choose_admin_action"
        #Entering action
        ##To do
        
    if state == "choose_admin_action":
        matrix.input_code = ""
        action = matrix.read_input("")
        if action == '1':
            LCD.lcd.clear()
            LCD.lcd.cursor_pos = (0,0)
            LCD.lcd.write_string("Enrolling mode")
            LCD.lcd.cursor_pos = (1,0)
            LCD.lcd.write_string("Place finger")
            fingerprint.enrollFinger(CONFIRM_BUTTON)
                
                

        if action == '2':
            LCD.lcd.clear()
            # LCD.lcd.cursor_pos = (0,0)
            # LCD.lcd.write_string("Delete mode")
            LCD.lcd.cursor_pos = (0,0)
            LCD.lcd.write_string("Enter emp to delete")
            fingerprint.delete_employer(CONFIRM_BUTTON)
        
    if state == "user_mode":
        verdict = fingerprint.search_finger()
        time.sleep(0.5)
        if verdict == False:
            buzzer.incorrect_beep()
            LED.blink_red()
            LCD.lcd.clear()
            LCD.lcd.cursor_pos = (0, 0)
            LCD.lcd.write_string("Not Found")
            LCD.lcd.cursor_pos = (1, 0)
            LCD.lcd.write_string("Try again!")
            time.sleep(3)
            state = "mode_choosing"
            LCD.hello_screen()
        elif verdict != False:
            name, surname, sec_level = verdict
            local_ip = socket.gethostbyname(socket.gethostname()) ##ip
            zone = DB.fetch_zone_by_ip(local_ip)
            #[time] Zone: [Zone] Employer: [name surname] Access: [Granted | Not Granted]
            if DB.fetch_sec_level(local_ip) > int(sec_level): ## Comparison room security level and employee security level
                buzzer.incorrect_beep()
                LED.blink_red()
                LCD.lcd.clear()
                LCD.lcd.cursor_pos = (0,0)
                LCD.lcd.write_string("Access denied")
                DB.insert_event(name, surname, zone, access='Denied')
                Log.print_last_event()
                time.sleep(3)
                state = "mode_choosing"
                LCD.hello_screen()
            else:
                buzzer.correct_beep()
                LED.blink_green()
                LCD.lcd.clear()
                LCD.lcd.cursor_pos = (0,0)
                servo.open_lock()
                LCD.lcd.write_string(f"Welcome, {name} {surname}")
                DB.insert_event(name, surname, zone, access='Granted')
                Log.print_last_event()
                time.sleep(3)
                #print(f"Welcome, {name} {surname}")
            state = "mode_choosing"
            LCD.hello_screen()
            
        
        









    






