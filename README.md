# Blockchain4E2CC

Blockchain for Edge to Cloud Continuum

# Draft Architecture

![Alt Draft Architecture](docs/architecture_draft_v2.png "Draft Architecture")

# Overview

We would need to setup two blockchain networks - one to host the fognode servers and another to store the hashed values from the sensors. In the steps that follow, we would be generating some data from one or more sensors, send them to the fog node, the fognode sends them to some blockchain network where their meta data are hashed and stored. The data is then stored off chain on minio.

# Installation

While the draft architecture proposes puting the `fognode blockchain Network`, the `main blockchain network` and the `Cloud Rspository` on different servers, you can install them all one server for testing purposes.

You would to ensure you have Python3.x installed locally on your test machine.

To install the prerequsites, clone the repository and run the ansible playbook contained in `ansible/`. You would have to set the `ip address` of the host in `ansible/inventory/hosts.yaml`. This playbook also installs and sets up the `minio` server.

```
cd ansible
ansible-playbook setup-host.yaml -i inventory/hosts.yaml

```

To setup the main blockchain network, again, you would have to set the `ip address` of the host in `ansible/inventory/hosts.yaml` and

```
cd ansible
ansible-playbook setup-fabric.yaml -i inventory/hosts.yaml

```

To setup the the fog node blockchain network,

```
cd fognode/fablo
fablo up fablo-config.json
```

To setup the main blockchain network

```
cd fablo
fablo up fablo-config.json
```

The networks setup should take a while to complete.

If the commands above all complete successfully, you should have two Fabric networks.

1. A blockchain that hosts the fog environment with just one organization and two peers
2. A main blockchain with five organizations having two peers each. This network has 2 orderers

Now, it time to do some testing!!

# Registering Sensors on the Fog Node

Before the Fognode can accept any sensor data, that sensor needs to be registered on the fognode otherwise the fognode would drop all data from such a sensor.

First, we would need to enroll a user on the fognode blockchain. `127.0.0.1` can be changed to the ip address of the machine running the fognode blockchain network

```
curl --location --request POST 'http://127.0.0.1:8801/user/enroll' \
--header 'Authorization: Bearer' \
--header 'Content-Type: text/plain' \
--data-raw '{"id": "admin", "secret": "adminpw"}'

```

We should get an authorization token as a response, that would be needed for the next command

Next, we register the sensor on the fognode blockchain network. In this example, we would be registering sensor-one belonging to some organization.

```
curl --location --request POST 'http://127.0.0.1:8801/invoke/fognodechannel/fognode' \
--header 'Authorization: Bearer 671da960-8b38-11ed-8e65-d70eccfee9d0-admin' \
--header 'Content-Type: application/json' \
--data-raw '{
  "method": "KVContract:registerSensor",
  "args": [
    "TartuCityCouncil:sensorOne",
    "TartuCityCouncil:sensorOne@ut"
  ]
}

```

You should get back

```
{
    "response": {
        "success": "Ok: Sensor Registered on Network"
    }
}

```

Optional: Note, you would have to repeat the same process as above when registering other sensors.

# Generating Sensor Data

We have now registered a sensor, to generate some sample sensor data and send such to the fognode for onwards delivery to the blockchain network, you would have to run the sensor python script. In this example, we would be emulating data from sensor-one

```

cd sensors/tartucitycouncil/sensor-one
py app.py

```

Mock Sensor data should now be generated and sent to the fognode. You should see some logs

![Alt Sensor One Log](docs/sensor-one-log.png "Sensor One Log")
