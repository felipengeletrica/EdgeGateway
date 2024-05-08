#!/usr/bin/env python
#-*- coding: latin-1 -*-

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
        :type description: Name logger in test
        :type database: database
        """

        try:
            threading.Thread.__init__(self)

            print("New instance logging"), description
            self.s = None
            self.baudrate = None
            self.port = None
            self.timeout = None
            self.connState = False
            self.description = description

            # Criar uma instância de MqttManager com a função de callback
            self.mqtt_manager = MqttManager(
                username=server_mqtt['username'],
                password=server_mqtt['password'],
                server=server_mqtt['server'],
                port=server_mqtt['port'],
                client='client1',
                subscribe=server_mqtt['subscribe'])

            self.subscribe = server_mqtt['subscribe']

        except:
            raise

    def run(self, port, baudrate, timeout):

        """
        Start thread for data processpath
        :type port: serial port conection ex. /dev/ttyUSB
        :type baudrate: 115200
        :type timeout: time for response
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

        try:
            if self.connState is True:
                self.s = None
                self.connState = False
        except:
            self.connState = False
            raise

    def serialstate(self):
        return self.connState

    def receivedata(self):

        while True:
            try:
                data = self.s.readline().decode()
                if len(data):
                    try:
                        json_obj = json.loads(data)
                        self.mqtt_manager.publish(self.subscribe, data)
                        if debug is True:
                            print(f'{json_obj} [{str(datetime.datetime.now())}]')
                    except json.JSONDecodeError:
                        print("Invalid json")
                        raise
            except Exception as error:
                self.connState = False
                print("exception data: ", error)
                raise
