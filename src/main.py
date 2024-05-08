#!/usr/bin/env python3
# coding=utf-8
"""
    Main program for datalogger interface
"""

# region import
import datetime
import time
import json
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
script_path = os.path.dirname(os.path.abspath(__file__))
parent_path = os.path.abspath(os.path.join(script_path, os.pardir))

from src.interface.SerialLogger import logger
from src.interface.BluetoothGpsAgrinavi import BluetoothGpsAgrinavi
from src.interface.BLEConnector import BLEConnector
from src.interface.mqtt_manager import MqttManager
# endregion




def handle_message(message_content):
    print("Received message:", message_content)


def LoadJSON():

    try:
        # Load configurations using file JSON
        with open(parent_path + '/config.json') as json_data_file:
            data = json.load(json_data_file)

    except Exception as error:
        print("Fail in open JSON File")
        raise error

    return data


def init_data_instances(datajson):

    """
        Load file of configuration and start multiples instances serial datalooger
    """


    server_mqtt = datajson["server_mqtt"]

    print(server_mqtt)

    if server_mqtt is not None:
        # Criar uma instância de MqttManager com a função de callback
        mqtt_manager = MqttManager(
            username=server_mqtt['username'], 
            password=server_mqtt['password'], 
            server=server_mqtt['server'], 
            port=server_mqtt['port'],
            client='client1', 
            subscribe=server_mqtt['subscribe'],
            message_callback=handle_message)
        
        mqtt_manager.start()  # Iniciar o cliente MQTT


    try:

        # After JSON LOAD
        devices = datajson['devices']

        timestamp = str(datetime.datetime.now())
        print(f"Start Server Logging {timestamp}")
        
        devs = list()
        
        # Create threads for instances in datalogger
        for index in range(0, len(devices)):
            print(f"Devices:{devices[index]['description']} Interface:{devices[index]['interface']}")

            # Serial Interface
            if "serial" in devices[index]['interface']:
                devs.append(
                    logger(
                        description=devices[index]['description'])
                )
                # Execute process
                devs[index].run(
                    port=devices[index]['serialport'],
                    baudrate=devices[index]['baudrate'],
                    timeout=devices[index]['timeout'])

            elif "serial-to-mqtt" in devices[index]['interface']:
                devs.append(
                    logger(
                        description=devices[index]['description'])
                )
                # Execute process
                devs[index].run(
                    port=devices[index]['serialport'],
                    baudrate=devices[index]['baudrate'],
                    timeout=devices[index]['timeout'])

            # Bluetooth interface
            elif "bluetooth-gps" in devices[index]['interface']:
                devs.append(
                    BluetoothGpsAgrinavi(
                        description=devices[index]['description'],
                        timeIgnoreData=devices[index]['samplingSeconds']))
                devs[index].run(
                    port=devices[index]['port'],
                    address=devices[index]['address']
                )

            # Bluetooth BLE interface
            elif "bluetooth-BLE" in devices[index]['interface']:

                devs.append(
                    BLEConnector(
                        device_name=devices[index]['description']
                    )
                )
                devs[index].run(
                    mac_address=devices[index]['mac-address']
                )
            else:
                Exception("Invalid device")
        a = 1
    except Exception as error:
        raise error


def main():

    print ("###############  Server Tests ########################")
    data_json = LoadJSON()

    init_data_instances(data_json)

    while True:

        try:

            keepAliveTimestamp = str(datetime.datetime.now())
            print(f"Keep Alive Datalogger {keepAliveTimestamp} \n\r")
            time.sleep(10)
        except Exception as error:
            print("Error: ", error)

if __name__ == "__main__":
    main()