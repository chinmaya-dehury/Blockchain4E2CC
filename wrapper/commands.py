
from utils import list_sensors, add_org
import requests
import os
import subprocess as sp

# https://www.pythonescaper.com/
# docker exec cli.tartucitycouncil.example.com peer chaincode invoke  -C "tartucitycouncilchannel" -n tartucitycouncil -c '{"Args":["KVContract:get", "Iwada Eja"]}'


class Commands:

    def __init__(self):
        super().__init__()

    def add_org(self, org_name, channel_name, chaincode_name, instance_count):
        add_org(org_name, channel_name, chaincode_name, instance_count)

    def org_channels(self, name):
        print("Commands: org_channels")

    def create_channel(self, name):
        print("Commands: create_channel")

    def add_to_channel(self, name, org):
        print("Commands: add_to_channel")

    def list_org_sensors(self, name):
        print("Commands: list_org_sensors")

    def add_sensor(self, name, org):
        print("Commands: add_sensor")

    def list_sensors(self):
        return list_sensors()

    def post_data(self, org, channel, chaincode, sensor):
        url = f"http://0.0.0.0:5001/{sensor}/api/v1.0/data"
        r = requests.get(url)
        data_key = r.json().get("data").get("timestamp")
        data_value = r.json().get("data").get("temperature")
        data = {'channel': channel, 'chaincode': chaincode,
                'key': data_key, 'value': data_value}
        payload = "docker exec {} peer chaincode invoke  -C \"{}\" -n {} -c \'{{\"Args\":[\"KVContract:put\", \"{}\", \"{}\"]}}\'".format(
            org, channel, chaincode, data_key, data_value)
        print("Sending data to the blockchain...", data)
        result = os.system(payload)
        print("Data sent successfully" if result == 0 else "Data not sent")

    def get_data(self, org, channel, chaincode, data_key):
        payload = "docker exec {} peer chaincode invoke  -C \"{}\" -n {} -c \'{{\"Args\":[\"KVContract:get\", \"{}\"]}}\'".format(
            org, channel, chaincode, data_key)
        # result = os.system(payload)
        # print(result)
        result = sp.getoutput(payload)
        print(result)
        print(
            "Data retrieval successfull" if "error" not in result else "Data not retrieved")

# docker exec cli.tartucitycouncil.example.com peer chaincode invoke  -C "tartucitycouncilchannel" -n tartucitycouncil -c '{"Args":["KVContract:get", "15:25:03"]}'
# docker exec cli.tartucitycouncil.example.com peer chaincode invoke  -C "tartucitycouncilchannel" -n tartucitycouncil -c '{'Args':["KVContract:put", "name", "Iwada Eja"]}'
