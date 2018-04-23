import telepot
import time
import wiringpi
import re
import sqlite3
from os.path import isfile
import picamera


#=============== Database =====================
database_file = 'aircon_controller.db'

if(not isfile(database_file)):
    # -- make database --

    #connect to db file
    conn = sqlite3.connect(database_file)
    c = conn.cursor()

    #make user table
    c.execute('CREATE TABLE users (user_id INTEGER PRIMARY KEY)')

    #add primary users
    users = [(367583792,)]
    c.executemany('INSERT INTO users VALUES (?)', users)

    #commit and close
    conn.commit()
    conn.close()

def get_authed_users():
    #connect to db file
    conn = sqlite3.connect(database_file)
    c = conn.cursor()

    #make user table
    c.execute('SELECT * FROM users')
    res = c.fetchall()
    return [row[0] for row in res]

def add_authed_user(id_):
    #connect to db file
    conn = sqlite3.connect(database_file)
    c = conn.cursor()

    #add user
    users = [(id_,)]
    c.executemany('INSERT INTO users VALUES (?)', users)

    #commit and close
    conn.commit()
    conn.close()

#===================== Servo Setup =========================
# use 'GPIO naming'
wiringpi.wiringPiSetupGpio()
# set #18 to be a PWM output
wiringpi.pinMode(18, wiringpi.GPIO.PWM_OUTPUT)
# set the PWM mode to milliseconds stype
wiringpi.pwmSetMode(wiringpi.GPIO.PWM_MODE_MS)
# divide down clock
wiringpi.pwmSetClock(192)
wiringpi.pwmSetRange(2000)

def toggle(match, chat_id):
    wiringpi.pwmWrite(18, 100)
    time.sleep(1)
    wiringpi.pwmWrite(18, 200)
    bot.sendMessage(chat_id, "Toggled")
    wiringpi.pwmWrite(18, 0)

#===================== Camera Setup ========================
camera = picamera.PiCamera()

image_name = 'image.jpg'

#Settings (with defaults):
# camera.sharpness = 0
# camera.contrast = 0
camera.brightness = 50
# camera.saturation = 0
# camera.ISO = 0
# camera.video_stabilization = False
# camera.exposure_compensation = 0
# camera.exposure_mode = 'auto'
# camera.meter_mode = 'average'
# camera.awb_mode = 'auto'
# camera.image_effect = 'none'
# camera.color_effects = None
# camera.rotation = 0
# camera.hflip = False
# camera.vflip = False
# camera.crop = (0.0, 0.0, 1.0, 1.0)

def sendPic(match, chat_id):
    bot.sendMessage(chat_id, "Taking picture")
    camera.capture(image_name)
    pic = open(image_name, 'rb')
    bot.sendPhoto(chat_id, pic)


#================= Command Processing ======================
def add(match, chat_id):
    id_ = int(match.group(1))
    if(id_):
        try:
            add_authed_user(id_) #NEEDS TO BE TESTED
        except sqlite3.IntegrityError:
            msg = "That ID already exists"
        else:
            msg = "Added ID: {0}".format(id_)

        authed_users = get_authed_users()
    else:
        msg = "Please use /add follwed by a user id\ne.g. /add 1234567"

    bot.sendMessage(chat_id, msg)


#map of rejex to function name
commands = {re.compile('/add *([0-9]+)'):add,
            re.compile('/toggle'):toggle,
            re.compile('/picture'):sendPic}



authed_users = get_authed_users()


bot = telepot.Bot('371709969:AAEWOo45Ks8A2nygbHmfXcLKOwJDzBptWJY')

def handle(msg):
    chat_id = msg['chat']['id']
    command_text = msg['text']

    if(chat_id not in authed_users):
        bot.sendMessage(chat_id, "This is a private bot. To access, get a registered user to add your id with the command /add_id\nYour id is: {0}".format(chat_id))
    else:
        not_reconised = True
        for command in commands:
            match = command.match(command_text)
            if match:
                not_reconised = False
                commands[command](match, chat_id)
                break
        if(not_reconised):
            bot.sendMessage(chat_id, "Command not reconised.")





bot.message_loop(handle)
print('ready')

while 1:
    time.sleep(10)
