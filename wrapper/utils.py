import json
import os
import subprocess as sp
from datetime import datetime


def validate_arg(args):
    # Orgs and channel name must be alphanimeric and atleast 4 characters
    return args and str(args.lower()).isalpha() and len(args) > 3


def is_network_running(host):
    # check if network is running
    return True


def list_sensors():  # get this from dynamic source
    return {
        "sensor-one": {
            "id": "sensor-one",
            "name": "Sensor One",
            "description": "Temperature sensor",
            "org": "SolarPanelVendor",
            "endpoint": "http://localhost:5001/sensor-one/api/v1.0/data",
        },
        "sensor-two": {
            "id": "sensor-two",
            "name": "Sensor Two",
            "description": "Temperature sensor",
            "org": "SolarPanelVendor",
            "endpoint": "http://localhost:5002/sensor-two/api/v1.0/data",
        },
        "sensor-three": {
            "id": "sensor-three",
            "name": "Sensor Three",
            "description": "Temperature sensor",
            "org": "SolarPanelVendor",
            "endpoint": "http://localhost:5003/sensor-three/api/v1.0/data",
        },
    }


def generate_peer_list(instance_count):
    peer_list = []
    for i in range(0, int(instance_count)):
        peer_list.append(f"peer{i}")
    return peer_list


def build_fablo_json(org_name, channel_name, chaincode_name, instance_count, src_file_name="../fablo/fablo-config.json", dest_file_name="../fablo/fablo-config-{}.json".format(datetime.now().strftime("%Y%m%d%H%M%S"))):
    file_part = {
        "organization": {
            "name": f"{org_name}",
            "domain": f"{org_name}.example.com",
        },
        "peer": {
            "instances": int(instance_count),
            "db": "CouchDb",
        },
        "tools": {}
    }

    channel_to_add = {
        "name": f"{channel_name}",
        "orgs": [
            {
                "name": f"{org_name}",
                "peers": generate_peer_list(instance_count)
            }
        ]
    }

    chaincode_to_add = {
        "name": f"{chaincode_name}",
        "version": "0.0.1",
        "lang": "node",
        "channel": f"{channel_name}",
        "directory": "./chaincodes/chaincode-kv-node"
    }

    # Read JSON file
    with open(src_file_name) as fp:
        data = json.load(fp)
        data["orgs"].append(file_part)
        data["channels"].append(channel_to_add)
        data["chaincodes"].append(chaincode_to_add)
        # print(data["channels"][0].get("orgs")[0].get("peers") + ["peer2"])

    with open(dest_file_name, 'w') as file:
        json.dump(data, file, indent=4)

    return dest_file_name


def validate_config(config_file):
    # validate config file
    result = sp.getoutput(f"fablo validate {config_file}")
    if "Json schema validation failed!" in result:
        print("Invalid config file")
        return False
    return True


def add_org(org_name, channel_name, chaincode_name, instance_count):
    print("Adding org to network..")
    print("Generating fablo config file..")
    new_network_config_file = build_fablo_json(
        org_name, channel_name, chaincode_name, instance_count)
    print("Validating config file...")
    if not validate_config(new_network_config_file):
        return
    print("Tearing network...")
    sp.getoutput(f"fablo down {new_network_config_file}")
    print("Adding organizating and restarting network...")
    sp.getoutput(f"fablo up {new_network_config_file}")
    print("Network started successfully")

    print("Commands: add_org")


# build_fablo_json("avecitycouncil", "avecitycouncilchannel",
#                  "avechaincode", 2)

# print(validate_config("../fablo/fablo-config-new.json"))

# add_org("", "avecitycouncil", "avecitycouncilchannel",
#         "avechaincode", 2)
