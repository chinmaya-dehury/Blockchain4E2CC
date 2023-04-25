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
TOKEN_ENDPOINT = config['fog']['tokenendpoint']
USERID = config['fog']['userid']
USERSECRET = config['fog']['usersecret']
app = Flask(__name__)
TRANSMIT_INTERVAL = int(config['time']['one_second'])
API_ENDPOINT = f"{PROTOCOL}://{HOST}:{PORT}/{ENDPOINT}"
TOKEN_ENDPOINT = f"{PROTOCOL}://{HOST}:{PORT}/{TOKEN_ENDPOINT}"

ORG_NAME = config['orgs']['org1']
DEVICE_ID = 'sensorOne'


counter = 0

app = Flask(__name__)


def get_token():
    headers = {
        "Authorization": "Bearer ",
        "Content-Type": "application/json"
    }
    global token
    s = requests.Session()
    retries = Retry(total=50, backoff_factor=1,
                    status_forcelist=[502, 503, 504])
    s.mount('http://', HTTPAdapter(max_retries=retries))
    return s.post(url=TOKEN_ENDPOINT, headers=headers,
                  json={"id": USERID, "secret": USERSECRET}).json().get('token')


token = get_token()


def generate_temperature():
    # increment counter every second
    global counter
    global data
    while True:
        counter = counter + 1
        t = time.localtime()
        current_time = time.strftime("%Y-%m-%dT%H:%M:%SZ", t)
        current_temperture = 10 + random.random() * 10
        data = {
            "id": counter,
            "temperature": current_temperture,
            "timestamp": current_time,
            "org": ORG_NAME,
            "device": DEVICE_ID,
        }
        time.sleep(TRANSMIT_INTERVAL)
        post_to_gateway(data)


def post_to_gateway(data):
    global token
    print("Authenticating with token " + token)
    headers = {
        'Authorization': 'Bearer ' + token}
    s = requests.Session()
    retries = Retry(total=50, backoff_factor=1,
                    status_forcelist=[502, 503, 504])
    s.mount('http://', HTTPAdapter(max_retries=retries))
    blockchain_id = data['org'] + ":" + \
        data['device'] + ":" + data['timestamp']
    print("Sending with key ", blockchain_id)
    try:  # Not really needed as this only handles situations where the gateway is down while restarting the network
        response = s.post(url=API_ENDPOINT, headers=headers, json={
                          "method": "KVContract:put", "args": [blockchain_id, str(data)]})
        print(response.text)
        return response
    except Exception as e:
        print("Error sending data to gateway: ", e)


def get_free_tcp_port():
    tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    tcp.bind(('', 0))
    addr, port = tcp.getsockname()
    tcp.close()
    return port

# We enroll an admin user to the network and get a auth token back.
# We need to refresh the token every 10 minutes as we are using fablo and it has a 10 minute timeout for auth tokens
# https://github.com/fablo-io/fablo-rest/issues/35#issuecomment-1003977158


def refresh_token():
    print("Refreshing token")
    while True:
        global token
        token = get_token()
        time.sleep(540)  # 9 minutes


def start_web_server():
    app.run(host='0.0.0.0', port=get_free_tcp_port())


@ app.route('/sensor-one/api/v1.0/data', methods=['GET'])
def main():
    global counter
    global data
    return jsonify({'data': data})


if __name__ == "__main__":
    stateThread = threading.Thread(target=generate_temperature)
    stateThread.daemon = True
    stateThread.start()

    webThread = threading.Thread(target=start_web_server)
    webThread.start()

    tokenThread = threading.Thread(target=refresh_token)
    tokenThread.daemon = True
    tokenThread.start()
