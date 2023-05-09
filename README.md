# EC2-Block

E2C-Block is a proposed model
architecture that aims to provide an effective solution for managing and securing data
generated by IoT sensors in a distributed environment. It ensures that data generated by
these IoT sensors are securely transmitted and stored tamper-proof. The model comprises
two blockchain networks and an external data repository.

The first blockchain network is located in a fog computing environment close enough
to the IoT sensors generating the data. This Blockchain is called the Sensor Blockchain
Network(SBN). In the E2C-Block architecture, the fog computing environment provides
a secure communication channel between IoT devices and the cloud infrastructure. This SBN has peers that
process and transmits data to a second blockchain network in a
cloud computing environment.

The second blockchain network is the larger of the
two blockchain networks. It is located in a cloud computing environment. It is called
the Primary Blockchain Network(PBN). It receives IoT Sensor data from the SBN,
hashes and stores this hash of the sensor data on the ledger of its peers, and passes on
the originally received IoT sensor data to an external data repository. As discussed in
Section 3, this hashing process becomes useful when we check the integrity of the IoT’s
Sensors Data.

To store the vast amount of data generated by IoT sensors, the E2C-Block
architecture uses an offsite data store. This provides an optimal storage option as it allows
data to be stored in a secure and scalable manner

# See it in Action

[![How to use](docs/highlevel_overview_min.jpg)](https://youtu.be/pKvMTjo_5og)

# Architecture

![Alt Draft Architecture](docs/highlevel_overview_v2.jpg "EC2-Block Architecture")

# Overview

To Deploy EC2-Block, We would need to setup Two Blockchain networks - one to serve as the Sensor Blockchain network and another to serve as the Primary Blockchain Network. We would also need to set up the External Data Repository. In the steps that follow, we would be generating some data from one or more sensors, send them to the Sensor Blockchain Network that sends them off the the Primary Blockchain network where this data is hashed and the hash stored. The data is then stored off chain on the external data repository.

# Installation

You would need atleast two seperate servers to deploy the two Blockchain networks. The MinIO server can be on either of the servers, but preferably the server that hosts the Sensor Blockchain Network.

You would to ensure you have Python3.x installed locally on your test machine.

To install the prerequsites, clone the repository and run the ansible playbook contained in `ansible/`. You would have to set the `ip address` of the host in `ansible/inventory/hosts.yaml`. This playbook also installs and sets up the `minio` server.

```bash
cd ansible
ansible-playbook setup-host.yaml -i inventory/hosts.yaml

```

To setup the servers for the two blockchain networks, set their IPs in `ansible/inventory/hosts.yaml` and

```bash
cd ansible
ansible-playbook setup-fabric.yaml -i inventory/hosts.yaml

```

On the Server for the Sensor Blockchain Network, to setup the Sensor Blockchain Network, clone this repository,

```bash
git clone https://github.com/chinmaya-dehury/Blockchain4E2CC.git
cd Blockchain4E2CC/fognode/fablo
fablo up fablo-config.json
```

On the Second Server for the Primary Blockchain Network, to setup the Primary Blockchain Network, clone this repository

```bash
git clone https://github.com/chinmaya-dehury/Blockchain4E2CC.git
cd Blockchain4E2CC/fablo
fablo up fablo-config.json
```

Both Blockchain networks should take a while to setup. The Primary Blockchain network will take a little longer. .

If the commands above all complete successfully, you should have two Hyperledger Fabric networks.

# Starting Minio Server

As unhashed data would be stored offchain on `minIO`, we need to start the minio server. The minio server was setup when the first ansible playbook was ran. On the server running the MinIO,

```bash
MINIO_ROOT_USER=$MINIO_ROOT_USER MINIO_ROOT_PASSWORD=$MINIO_ROOT_PASSWORD minio server /mnt/data --console-address ":9001"

```

Where MINIO_ROOT_USER abd MINIO_ROOT_PASSWORD are enviroment variables of you choice. Next, generate(from the Minio Web interface) and set the following environment variables
MINIO_URL,MINIO_PORT,MINIO_ACCESS_KEY,MINIO_SECRET

![Alt Minio Web Console](docs/minio-web-console.png "Minio Web Console")

Now, it time to do some testing!!

# Registering Sensors on the Sensor Blockchain Network

Before the Sensor Blockchain Network can accept any sensor data, that sensor needs to be registered on the Sensor Blockchain network, otherwise all data from such a sensor will be dropped.

First, we would need to enroll a user on the fognode blockchain. `127.0.0.1` can be changed to the ip address of the machine running the Sensor blockchain network

```bash
curl --location --request POST 'http://127.0.0.1:8801/user/enroll' \
--header 'Authorization: Bearer' \
--header 'Content-Type: text/plain' \
--data-raw '{"id": "admin", "secret": "adminpw"}'

```

We should get an authorization token as a response, that would be needed for the next command

Next, we register the sensor on the Sensor blockchain network. In this example, we would be registering sensor-one belonging to some example organization.

```bash
curl --location --request POST 'http://127.0.0.1:8801/invoke/fognodechannel/fognode' \
--header 'Authorization: Bearer 671da960-8b38-11ed-8e65-d70eccfee9d0-admin' \
--header 'Content-Type: application/json' \
--data-raw '{
  "method": "KVContract:registerSensor",
  "args": [
    "example:sensorOne",
    "example:sensorOne@ut"
  ]
}

```

You should get back

```bash
{
    "response": {
        "success": "Ok: Sensor Registered on Network"
    }
}

```

Optional: Note, you would have to repeat the same process as above when registering other sensors.

# Generating Sensor Data

We have now registered a sensor, to generate some sample sensor data and send such to the fognode for onwards delivery to the blockchain network, you would have to run the sensor python script. In this example, we would be emulating data from sensor-one

```bash

cd sensors/example/sensor-one
py app.py

```

Mock Sensor data should now be generated and sent to the fognode. You should see some logs

![Alt Sensor One Log](docs/sensor-one-log.png "Sensor One Log")

# MinIO Web Interface

You can visit the Minio Server Web Console to see Mock data being recieved from the Main Blockchain after such data is hashed and stored.

![Sensor data](docs/minio-web-with-sensor-data.png "Sensor data")

We try to detail the flow of data from the sensors to the MinIO server with the image below

![Alt Sensor Flow](docs/data-flow-from-sensor-to-minio-v3.jpg "Sensor Flow")

# Query for Stored Sensor data

Query for Stored sensor data is done to the MinIO Server. We developed a simple interface that allows us to query and verify if the sensor data has been tampered with or not.

To run this interface,

```bash

cd query-interface/
py app.py

```
