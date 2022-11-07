
import rpyc
import time
import sys
import readline
from commands import Commands
from utils import is_network_running, validate_arg


def main():

    INFO = """commands:
    add-org <org-name> <channels-list> <chain-code> <peers-count> 
    org-channels <org-name>
    create-channel <channel-name>
    add-to-channel <org-name> <channel-name>
    list-sensors
    list-org-sensors <org-name>
    add-sensor <org-name> <sensor-name>
    post-data <org-name> <channel-name> <chain-code> <sensor-name> 
    get-data <org-name> <channel-name> <chain-code> <data-key>
    exit
    info
    """
    global HOST_PORT, HOST
    HOST_PORT = 7779
    HOST = "localhost"

    if not is_network_running('localhost'):
        print("A Network is not running")
        return

    running = True
    while running:
        command = input("\n$ ")
        args = None
        value = None
        command = command.split(' ')
        if (len(command) == 2):
            args = command[1]
        if (len(command) == 3):
            args = command[1]
            value = command[2]
        striped_command = command[0].rstrip()
        if striped_command == "add-org" and len(command) == 5:
            Commands.add_org(
                "", command[1], command[2], command[3], command[4])
            #Commands.add_org(args, command[2], command[3], command[4])
        # TODO validate all args here to avoid errors
        # NOTE: add-org avecitycouncil avecitycouncilchannel avechaincode 2
            # if validate_arg(args):
            #     print(command[1],  command[2], command[3], command[4])
            # else:
            #     print(
            #         f"Issue with the command - {args}. name must be alphanimeric and atleast 4 characters")
        elif striped_command == "org-channels" and len(command) == 2:
            if validate_arg(args):
                Commands.org_channels(" ", args)
            else:
                print(
                    f"Issue with the command - {args}. name must be alphanimeric and atleast 4 characters")

        elif striped_command == "create-channel" and len(command) == 2:
            if validate_arg(args):
                Commands.create_channel(" ", args)
            else:
                print(
                    f"Issue with the command - {args}. name must be alphanimeric and atleast 4 characters")

        elif striped_command == "add-to-channel" and len(command) == 3:
            if validate_arg(args):
                Commands.add_to_channel(" ", args, value)
            else:
                print(
                    f"Issue with the command - {args}. name must be alphanimeric and atleast 4 characters")

        elif striped_command == "list-sensors":
            print(
                f"{'id':<20}{'name':<20}{'description':<20}{'org':<20}{'endpoint':<20}")
            for sensor in Commands.list_sensors("").values():
                print(type(sensor))
                print(
                    f"{sensor['id']:<20}{sensor['name']:<20}{sensor['description']:<20}{sensor['org']:<20}{sensor['endpoint']:<20}")

        elif striped_command == "list-org-sensors" and len(command) == 2:
            # provide list docker containers with the name orgname?
            if validate_arg(args):
                Commands.list_org_sensors(" ", args)
            else:
                print(
                    f"Issue with the command - {args}. name must be alphanimeric and atleast 4 characters")

        elif striped_command == "add-sensor" and len(command) == 3:
            # Add sensor for an org. Probably just deploy some docker container, name would be orgname:sensorname
            if validate_arg(args):
                Commands.add_sensor(" ", args, value)
            else:
                print(
                    f"Issue with the command - {args}. name must be alphanimeric and atleast 4 characters")

        elif striped_command == "exit":
            print("Program exited.")
            running = False
            # kill the network ?
        elif striped_command == "post-data" and len(command) == 5:
            # get data from endpoint
            # Post data to a channel
            # post-data cli.tartucitycouncil.example.com tartucitycouncilchannel tartucitycouncil sensor-one
            Commands.post_data(
                " ", command[1],  command[2], command[3], command[4])
        elif striped_command == "get-data" and len(command) == 5:
            # get-data cli.tartucitycouncil.example.com tartucitycouncilchannel tartucitycouncil 15:25:03
            Commands.get_data(
                " ", command[1],  command[2], command[3], command[4])

        elif striped_command == "info" or striped_command == "ls":
            print(INFO)
        else:
            print(
                f"Invalid Command: {' '.join(command)}. type info for avaliable commands and their usage")


if __name__ == '__main__':
    main()
