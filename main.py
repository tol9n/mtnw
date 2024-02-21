import json
import requests
import time
from threading import Thread

data = {'online': True, 'rawTime': '', 'time': [0, 0], 'rain': True}


def timestamp():
    return str(time.time_ns())[:13]


def server_data():
    res = requests.get(f'https://tfc.su:8155/up/world/world/{timestamp()}')
    data['rawTime'] = str(res.json()['servertime'])
    data['rain'] = res.json()['hasStorm']


def server_time(inf: str):
    time = inf[:-1]
    time = '0' * (4 - len(time)) + time
    hour = int(time[:2]) + 6
    if hour >= 24:
        hour -= 24
    minutes = int(round(int(time[-2:]) * 0.6, 0))
    data['time'] = [hour, minutes]


def work():
    while True:
        try:
            server_data()
            server_time(data['rawTime'])
            data['online'] = True
            print(data)
        except requests.exceptions.ConnectionError:
            print('M_Connection trouble')
        except requests.exceptions.ReadTimeout:
            print('M_Server TIME OUT')
        except requests.exceptions.JSONDecodeError:
            data['online'] = False
            time.sleep(5)
        except KeyboardInterrupt:
            break


def serv():
    pass


if __name__ == '__main__':
    try:
        Thread(target=work).start()
        Thread(target=serv).start()
        print('Started...')
    except:
        print('error on starting')
