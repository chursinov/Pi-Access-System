import os
import DB_mod as DB
def print_last_event():
    if os.path.exists('/home/pi/Documents/test project/log.txt') == False:
        file = open('log.txt', 'w')
    else:
        file = open('log.txt', 'a')
    date,zone, person, access = DB.fetch_last_event()
    file.write("\n")
    file.write(f"[{date}] Zone: {zone}, Person: {person}, Access: {access}")
    file.close()