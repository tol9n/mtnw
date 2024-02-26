import json

import requests
import time
from threading import Thread
from flask import Flask

data = {'online': True, 'rawTime': '', 'time': [0, 0], 'rain': True}
app = Flask(__name__)


@app.route('/mtime/api/v0.1/')
def get():
    return json.dumps(data)


def timestamp() -> str:
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
        except requests.exceptions.ConnectionError:
            print('M_Connection trouble')
        except requests.exceptions.ReadTimeout:
            print('M_Server TIME OUT')
        except requests.exceptions.JSONDecodeError:
            data['online'] = False
            time.sleep(5)
        except KeyboardInterrupt:
            break


if __name__ == '__main__':
    from waitress import serve
    try:
        print('Started...')
        Thread(target=work).start()
        serve(app, host='0.0.0.0',port=5000)
    except:
        print('error on starting')
