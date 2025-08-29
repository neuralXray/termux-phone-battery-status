from sys import argv
from subprocess import run, PIPE
from json import loads
from time import sleep, time
from datetime import datetime

from telepot import Bot
from telepot.loop import MessageLoop


script = argv[0]
if '/' in script:
    script_path = script[:script.rindex('/') + 1]
else:
    script_path = ''

file = open(f'{script_path}phone_battery_status.conf', 'r')
lines = file.readlines()
file.close()

token = lines[0][:-1] 
receiver_id = lines[1]
if receiver_id[-1] == '\n':
    receiver_id = receiver_id[:-1]

bot = Bot(token)
printouts = []


def gather_battery_info():
    battery_info = run(['termux-battery-status'], stdout=PIPE)
    return loads(battery_info.stdout.decode('utf-8'))

def is_phone_unplugged(battery_info):
    plugged = battery_info['plugged']
    if plugged == 'UNPLUGGED':
        return True
    else:
        return False


def send_telegram_message(printout, send_date_time=True):
    global printouts
    if send_date_time:
        date_time = datetime.now().strftime('%b %d %H:%M:%S')
        printout = date_time + ' ' + printout
    if printouts:
        info = date_time + ' telegram connection reestablished'
        try:
            bot.sendMessage(receiver_id, info)
        except:
            pass
        for p in printouts.copy():
            try:
                bot.sendMessage(receiver_id, p)
                del printouts[0]
            except:
                break
    try:
        bot.sendMessage(receiver_id, printout)
    except:
        printouts.append(printout)


def handle(msg):
    try:
        received_msg = msg['text']
    except:
        pass
    if received_msg == 'status':
        battery_info = gather_battery_info()
        phone_unplugged = is_phone_unplugged(battery_info)
        if phone_unplugged:
            send_telegram_message('Phone unplugged')
        else:
            send_telegram_message('Phone plugged')
    elif received_msg == 'battery':
        battery_info = gather_battery_info()
        battery = battery_info['level']
        send_telegram_message(f'Battery level {battery}')
    elif received_msg == 'help':
        send_telegram_message('status', send_date_time=False)
        send_telegram_message('battery', send_date_time=False)


MessageLoop(bot, handle).run_as_thread()


previous_phone_unplugged = False
warned = False
t0 = time()
while True:
    battery_info = gather_battery_info()
    phone_unplugged = is_phone_unplugged(battery_info)
    if phone_unplugged and (not previous_phone_unplugged):
        send_telegram_message('Phone unplugged')
        previous_phone_unplugged = True
        warned = False
        t0 = time()
    elif (not phone_unplugged) and previous_phone_unplugged:
        send_telegram_message('Phone plugged')
        previous_phone_unplugged = False
    if previous_phone_unplugged:
        if (not warned) and (time() - t0 > 10*60):
            battery = battery_info['level']
            if battery < 90:
                send_telegram_message('Phone still unplugged')
                send_telegram_message(f'Battery level {battery}')
                warned = True
        sleep(1)
    else:
        sleep(10)

