import psycopg2
import LCD_mod as LCD
db_name = "skud"
db_user = "fingerprint"
db_address = "192.168.0.28"

def fetchFingers():
    conn = psycopg2.connect(f"dbname={db_name} user={db_user} host={db_address} password=127238349Tel")
    cur = conn.cursor()
    cur.execute(f"SELECT fingerprint.specs \
                FROM fingerprint \
                INNER JOIN employer \
                ON fingerprint.employer_id = employer.employer_id")
    res = cur.fetchall()
    if res == None:
        return False
    cur.close()
    conn.close()
    return res

def fetchFingersEmployersSecLevels():
    conn = psycopg2.connect(f"dbname={db_name} user={db_user} host={db_address} password=127238349Tel")
    cur = conn.cursor()
    cur.execute(f"SELECT fingerprint.specs, employer.name, employer.surname, employer.sec_level \
                FROM fingerprint \
                INNER JOIN employer \
                ON fingerprint.employer_id = employer.employer_id")
    res=cur.fetchall()
    return res


def addFingerPrint(specs,emp_id,sec_level):
    conn = psycopg2.connect(f"dbname={db_name} user={db_user} host={db_address} password=127238349Tel")
    str_specs = str(specs)
    cur = conn.cursor()
    cur.execute(f"SELECT count(*) FROM fingerprint \
                WHERE employer_id={emp_id}")
    res = cur.fetchone()
    if res[0] == 0:
        cur.execute(f"INSERT INTO fingerprint (specs,employer_id) \
                    VALUES (ARRAY {str_specs}, {emp_id})")
        cur.execute(f"UPDATE employer SET sec_level={sec_level} \
                    WHERE employer_id={emp_id}")
        conn.commit()
    else:
        return False
    cur.close()
    conn.close()
    return True

def delete_employer(id):
    conn = psycopg2.connect(f"dbname={db_name} user={db_user} host={db_address} password=127238349Tel")
    cur = conn.cursor()
    cur.execute(f"DELETE FROM employer \
                WHERE employer_id={id}")
    conn.commit()
    LCD.lcd.cursor_pos = (2,0)
    LCD.lcd.write_string("Commited to DB!")
    cur.close()
    conn.close()