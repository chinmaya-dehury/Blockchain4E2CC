import configparser
import socket
import threading
from flask import Flask
import random
import time
import requests
import logging
from flask import Flask, jsonify
from requests.adapters import HTTPAdapter, Retry

logging.basicConfig(level=logging.DEBUG)


config = configparser.ConfigParser()
config.read('../../../config.ini')

HOST = config['fog']['host']
PORT = int(config['fog']['port'])
PROTOCOL = config['fog']['protocol']
ENDPOINT = config['fog']['endpoint']
app = Flask(__name__)
TRANSMIT_INTERVAL = int(config['time']['twenty_seconds'])
API_ENDPOINT = f"{PROTOCOL}://{HOST}:{PORT}/{ENDPOINT}"

ORG_NAME = config['orgs']['org1']
DEVICE_ID = 'sensortwo'


counter = 0
app = Flask(__name__)


def generate_humidity():
    # increment counter every second
    global counter
    global data
    while True:
        counter = counter + 1
        t = time.localtime()
        # current_time = time.strftime("%H:%M:%S", t)
        current_time = time.strftime("%Y-%m-%dT%H:%M:%SZ", t)
        current_humidity = 50 + random.random() * 30
        data = {
            'id': counter,
            'humidity': current_humidity,
            'timestamp': current_time,
            'org': ORG_NAME,
            'device': DEVICE_ID,
        }
        time.sleep(TRANSMIT_INTERVAL)
        post_to_gateway(data)
        # print(data)


def post_to_gateway(data):
    s = requests.Session()
    retries = Retry(total=50, backoff_factor=1,
                    status_forcelist=[502, 503, 504])
    s.mount('http://', HTTPAdapter(max_retries=retries))
    return s.post(url=API_ENDPOINT, json=data)


def get_free_tcp_port():
    tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    tcp.bind(('', 0))
    addr, port = tcp.getsockname()
    tcp.close()
    return port


def start_web_server():
    app.run(host='0.0.0.0', port=get_free_tcp_port())


@ app.route('/sensor-one/api/v1.0/data', methods=['GET'])
def main():
    global counter
    global data
    return jsonify({'data': data})


if __name__ == "__main__":
    stateThread = threading.Thread(target=generate_humidity)
    stateThread.daemon = True
    stateThread.start()

    webThread = threading.Thread(target=start_web_server)
    webThread.start()
