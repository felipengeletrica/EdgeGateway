#!/usr/bin/env python
# -*- coding: latin-1 -*-

import serial
import time
import datetime
import threading
import json
import re
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
script_path = os.path.dirname(os.path.abspath(__file__))
parent_path = os.path.abspath(os.path.join(script_path, os.pardir))

from src.interface.mqtt_manager import MqttManager

debug = True


class SerialToMQTT(threading.Thread):

    def __init__(self, description, server_mqtt):

        """
        Initialize SerialToMQTT instance.

        :param description: Name SerialToFile in test
        :type description: str
        :param server_mqtt: MQTT server configuration
        :type server_mqtt: dict
        """

        try:
            threading.Thread.__init__(self)

            print("New instance gateway SERIAL <-> MQTT"), description
            self.s = None
            self.baudrate = None
            self.port = None
            self.timeout = None
            self.connState = False
            self.description = description

            # Create an instance of MqttManager with the callback function
            self.mqtt_manager = MqttManager(
                username=server_mqtt['username'],
                password=server_mqtt['password'],
                server=server_mqtt['server'],
                port=server_mqtt['port'],
                client='client1',
                subscribe_upstream=server_mqtt['subscribe-upstream'],
                subscribe_downstream=server_mqtt['subscribe-downstream'],
                on_message_callback=self.senddata)

            self.subscribe_upstream = server_mqtt['subscribe-upstream']
            self.subscribe_downstream = server_mqtt['subscribe-downstream']

        except:
            raise

    def run(self, port, baudrate, timeout):

        """
        Start thread for data processpath.

        :param port: Serial port connection, e.g., /dev/ttyUSB
        :type port: str
        :param baudrate: Baud rate, e.g., 115200
        :type baudrate: int
        :param timeout: Time for response
        :type timeout: int
        """
        #print "Starting " + self.name
        self.baudrate = baudrate
        self.port = port
        self.timeout = timeout
        self.mqtt_manager.run()
        self._process = p = threading.Thread(target=self._process)
        p.daemon = True
        p.start()

    def _process(self):

        """
        Internal method for processing data.
        """

        while True:
            try:
                if self.serialstate() is False:
                    self.connect(self.port, self.baudrate, self.timeout)
                    self.connState = True
                else:
                    self.receivedata()
            except:
                self.connState = False
                self.disconnect()
                #raise
            time.sleep(1)

    def connect(self, port, baudrate, timeout, rtscts=False, dsrdtr=False):

        """
        Connect to a serial port.

        :param port: Serial port connection, e.g., /dev/ttyUSB
        :type port: str
        :param baudrate: Baud rate, e.g., 115200
        :type baudrate: int
        :param timeout: Time for response
        :type timeout: int
        :param rtscts: Enable RTS/CTS flow control (default False)
        :type rtscts: bool
        :param dsrdtr: Enable DSR/DTR flow control (default False)
        :type dsrdtr: bool
        """

        try:
            self.baudrate = baudrate
            self.port = port
            self.timeout = timeout

            self.s = serial.Serial(port, baudrate=baudrate, timeout=timeout, rtscts=rtscts, dsrdtr=dsrdtr)
            self.connState = self.s.isOpen()

            if debug is True:
                print("Baudrate: ", self.baudrate)
                print("Port: ", self.port)
                print("Timeout: {0} ms".format(self.timeout))

        except Exception as error:
            self.connState = False
            print(error)
            raise

    def disconnect(self):

        """
        Disconnect from the serial port.
        """

        try:
            if self.connState is True:
                self.s = None
                self.connState = False
        except:
            self.connState = False
            raise

    def serialstate(self):
        """
        Check the state of the serial connection.
        """
        return self.connState

    def receivedata(self):

        """
        Receive data from the serial port and publish it to MQTT.
        """

        while True:
            try:
                data = self.s.readline().decode()
                # First verification json
                if len(data) and "{" in data and ":" in data:
                    # try parse to json to validate
                    try:
                        json_obj = json.loads(data)
                        # Add metadata with timestamp
                        metadata = {"timestamp": str(datetime.datetime.now())}
                        payload = {"gateway_meta": metadata, "data": json_obj}
                        payload_dumps = json.dumps(payload)
                        self.mqtt_manager.publish(self.subscribe_upstream, payload_dumps)
                        if debug is True:
                            print(f'{payload_dumps} [{str(datetime.datetime.now())}]')
                    except json.JSONDecodeError:
                        print("Invalid json")
                        raise
            except Exception as error:
                self.connState = False
                print("exception data: ", error)
                raise

    def senddata(self, message_content):
        """
        Send data via serial and print the message content.
        """
        try:
            if self.serialstate():
                try:
                    if isinstance(message_content, dict):
                        if 'raw' in message_content:
                            raw_value = message_content.get("raw")
                            self.s.write(raw_value.encode())
                            print(f"Message RAW via serial:{raw_value}")
                        else:
                            message_json = json.dumps(message_content)
                            self.s.write(message_json.encode())
                            print("Sent via serial:", message_content)
                    else:
                        print("message_content is not a dictionary.")
                except Exception as error:
                    print("Error sending data via serial:", error)
            else:
                print("Serial connection is not open.")
        except Exception as error:
            print("Error sending data via serial:", error)
