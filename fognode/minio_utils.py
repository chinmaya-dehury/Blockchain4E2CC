import io
import json

from datetime import datetime
import os
import random
import time
from iterators import TimeoutIterator
from minio import Minio


class MiniOClient:

    def __init__(self, endpoint, access_key, secret_key):
        self.client = Minio(endpoint,
                            access_key=access_key,
                            secret_key=secret_key,
                            secure=False)

    #
    def put_json(self, minio_client, bucket_name, object_name, d):
        """
        jsonify a dict and write it as object to the bucket
        """

        # create a new bucket, if not existing yet
        if not minio_client.client.bucket_exists(bucket_name):
            minio_client.client.make_bucket(bucket_name, location="eu-west-1")

        # prepare data and corresponding data stream
        data = json.dumps(d).encode("utf-8")
        data_stream = io.BytesIO(data)
        data_stream.seek(0)

        # put data as object into the bucket
        minio_client.client.put_object(
            bucket_name=bucket_name,
            object_name=object_name,
            data=data_stream, length=len(data),
            content_type="application/json"
        )

    def get_json(self, minio_client, bucket_name, object_name):
        """
        get stored json object from the bucket
        """
        data = minio_client.client.get_object(bucket_name, object_name)
        return json.load(io.BytesIO(data.data))

    def object_pooling(self, minio_client, bucket_name):
        """ As this is a blocking call, we need to run it in a thread and as such we need to have a list of objects that have not been processed to send to the blockchain"""
        posted_objects = set()
        print("object_pooling", bucket_name)
        """
        listen to a bucket for new objects
        """
        with minio_client.client.listen_bucket_notification(bucket_name) as events:
            it = TimeoutIterator(events, timeout=500)
            for event in it:
                if event is it.get_sentinel():
                    print("Sentinel received")
                    break
                else:
                    # self.get_json(minio_client, bucket_name, event.object_name)
                    bucket_name_l = event['Records'][0]['s3']['bucket']['name']
                    object_name_l = event['Records'][0]['s3']['object']['key']
                    if object_name_l not in posted_objects:
                        posted_objects.add(object_name_l)
                        print("object_pooling", bucket_name_l, object_name_l)
                        packaged_json = self.get_json(
                            minio_client, bucket_name_l, object_name_l)
                        self.send_to_blockchain(packaged_json)

    def send_to_blockchain(self, data):
        print("Sending to blockchain", data)

        t = time.localtime()
        send_to_blockchain_time = time.strftime("%Y-%m-%dT%H:%M:%SZ", t)

        # * @PS What should be the ID of the blockchain object?
        # * currently using the organization name and the device ID and timestamp
        blockchain_device_id = data['org'] + ":" + \
            data['device'] + ":" + time.strftime("%H:%M:%S", t)
        blockchain_data_value = {
            "generationTimeStamp": data['timestamp'],
            "deviceID": data['org'] + ":" + data['device'],
            "sendToBlockchainTime": send_to_blockchain_time,
            "action": "writeOperation",
        }

        blockchain_org = f"cli.{data['org']}.ie.io".lower()
        blockchain_channel = f"{data['org']}channel".lower()
        blockchain_chaincode = f"{data['org']}".lower()

        print(blockchain_org, blockchain_channel,
              blockchain_chaincode, blockchain_device_id)
        print("blockchain_data_value", blockchain_data_value)
        payload = "docker exec {} peer chaincode invoke  -C \"{}\" -n {} -c \'{{\"Args\":[\"KVContract:put\", \"{}\", \"{}\"]}}\'".format(
            blockchain_org, blockchain_channel, blockchain_chaincode, blockchain_device_id, blockchain_data_value)
        # TODO: * @self: This is a temporary solution to send the data to the blockchain. Send post requests via the Fablo REST API
        result = os.system(payload)
        print("sent successfully" if result == 0 else "not sent")
