#!/usr/bin/env python
#-*- coding: latin-1 -*-

#Copyright (c) 2017, Felipe Vargas <felipeng.eletrica@gmail.com>
#All rights reserved.
#
#Redistribution and use in source and binary forms, with or without
#modification, are permitted provided that the following conditions are met:
#
#1. Redistributions of source code must retain the above copyright notice, this
#   list of conditions and the following disclaimer.
#2. Redistributions in binary form must reproduce the above copyright notice,
#   this list of conditions and the following disclaimer in the documentation
#   and/or other materials provided with the distribution.
#
#THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
#ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
#WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
#DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE FOR
#ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
#(INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
#LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
#ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
#(INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
#SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#
#The views and conclusions contained in the software and documentation are those
#of the authors and should not be interpreted as representing official policies,
#either expressed or implied, of the FreeBSD Project.

import serial
import time
import datetime
import threading
import re


debug = False

from Dataanalysis import DataAnalysis


class logger(threading.Thread):

    def __init__(self, description):

        """
        :type description: Name logger in test
        :type database: database
        """

        try:
            threading.Thread.__init__(self)

            print "New instance logging", description
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
        Start thread for data processpath
        :type port: serial port conection ex. /dev/ttyUSB
        :type baudrate: 115200
        :type timeout: time for response
        """
        #print "Starting " + self.name
        self.baudrate = baudrate
        self.port = port
        self.timeout = timeout

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
                print "Baudrate: ", self.baudrate
                print "Port: ", self.port
                print "Timeout: {0} ms".format(self.timeout)

        except Exception as error:
            self.connState = False
            print error
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

        header = "[" + self.description + " ] "

        dataanalysis = DataAnalysis()

        while True:

            try:

                data = self.s.readline()
                #print data
                if len(data):

                    #if debug is True:
                        #print 'Data: ', data

                    log = '{0} {1}'.format(header, re.sub('[^A-Za-z0-9]+', ' ', data))

                    if debug is True:
                        print log + '[' + str(datetime.datetime.now()) + ']'

                    # Data analysis class
                    dataanalysis.processdata(log, self.description)

            except Exception as error:

                self.connState = False
                print "exception data: ", error
                raise