# # ref code snippet adapted from https://stackoverflow.com/a/39337670


import time
from minio_utils import MiniOClient
import threading
from flask import Flask, request, jsonify
import sys
import os
import requests


app = Flask(__name__)


ACCESS_KEY = os.environ.get('MINIO_ACCESS_KEY')
SECRET_KEY = os.environ.get('MINIO_SECRET')
minio_client = MiniOClient(
    "127.0.0.1:9000", ACCESS_KEY, SECRET_KEY)


def process_event():
    global data
    global message_flag
    message_flag = ''
    data = {}
    # We start a bucket listetning thread for each bucket. So we add the bucket to a set, and only create a thread if the bucket is not in the set.
    bucket_list = set()
    while True:
        if data:
            print("Processing  event", data)
            bucket_name = (data['org'] + data['device'] + 'Bucket').lower()
            object_name = "json/" + str(data['timestamp']) + '-' + data['org'] + '-' + \
                data['device'] + '-' + str(data['timestamp']) + '.json'
            minio_client.put_json(
                minio_client, bucket_name, object_name, data)
            if bucket_name not in bucket_list:
                bucket_list.add(bucket_name)
                t = threading.Thread(target=bucket_pooling, args=(
                    minio_client, bucket_name))
                t.start()
            data.clear()
            print(bucket_list)

# TODO: Should i pass the mionio_client as an argument?


def bucket_pooling(_, bucket_name):
    while True:
        print("Pooling for bucket", bucket_name)
        minio_client.object_pooling(minio_client, bucket_name)


def start_web_server():
    app.run(host='0.0.0.0', port=6001)


@ app.route('/gateway/kamoni/api/v1.0/process', methods=['POST'])
def main():
    global data
    print(
        f"Received data from ORG - {request.json.get('org')}:::{request.json.get('device')}")
    data = request.get_json()
    return jsonify({'data': 'data received'})


if __name__ == "__main__":
    stateThread = threading.Thread(target=process_event)
    stateThread.daemon = True
    stateThread.start()

    webThread = threading.Thread(target=start_web_server)
    webThread.start()
