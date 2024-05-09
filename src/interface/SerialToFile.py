#!/usr/bin/env python
# -*- coding: latin-1 -*-

import serial
import time
import datetime
import threading
from src.storage.Dataanalysis import DataAnalysis


debug = False

class SerialToFile(threading.Thread):
    """
    Class for logging data from serial port to a file.
    """

    def __init__(self, description):
        """
        Constructor for SerialToFile.

        :param description: Name SerialToFile in test
        :type description: str
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

        except:
            raise

    def run(self, port, baudrate, timeout):
        """
        Start thread for data processpath.

        :param port: serial port connection ex. /dev/ttyUSB
        :type port: str
        :param baudrate: 115200
        :type baudrate: int
        :param timeout: time for response
        :type timeout: int
        """
        self.baudrate = baudrate
        self.port = port
        self.timeout = timeout

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

        :param port: serial port connection ex. /dev/ttyUSB
        :type port: str
        :param baudrate: 115200
        :type baudrate: int
        :param timeout: time for response
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
        Receive data from the serial port and process it.
        """
        header = "[" + self.description + " ] "

        dataanalysis = DataAnalysis()

        while True:

            try:

                data = self.s.readline().decode()
                #print(data)
                if len(data):

                    log = data.strip()
                    if debug is True:
                        print(log + '[' + str(datetime.datetime.now()) + ']')

                    # Data analysis class
                    dataanalysis.processdata(log, self.description)

            except Exception as error:

                self.connState = False
                print("exception data: ", error)
                raise
