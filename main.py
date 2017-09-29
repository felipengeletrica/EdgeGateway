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

# "A universal convention supplies all of maintainability, clarity,
# consistency, and a foundation for good programming habits too.
# What it doesn't do is insist that you follow it against your will. That's Python!"
#
#  Tim Peters on comp.lang.python, 2001 - 06 - 16

import datetime
import time
import json
import os
import sys

from SerialLogger import logger

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
script_path = os.path.dirname(os.path.abspath(__file__))

def LoadJASON():

    try:
        # Load configurations using file JSON
        with open(script_path + '/config.json') as json_data_file:
            data = json.load(json_data_file)

    except Exception as error:
        print "Fail in open JSON File"
        raise error

    return data


def init_data_instances(datajson):

    """
        Load file of configuration and start multiples instances serial datalooger
    """

    try:

        # After JSON LOAD
        devices = datajson['devices']

        timestamp = str(datetime.datetime.now())
        message = "Start Server Logging {0} ".format(timestamp)
        print message

        devs = list()
        # Create threads for instances in datalogger
        for index in range(0, len(devices)):
            print "Devices:{0}".format(devices[index]['description'])
            devs.append(logger(devices[index]['description'] + " " + timestamp))
            devs[index].run(devices[index]['serialport'], devices[index]['baudrate'], devices[index]['timeout'])
    except Exception as error:

        raise error


def main():

    print "###############  Server Tests ########################"
    data_json = LoadJASON()

    init_data_instances(data_json)

    while True:

        try:

            keepAliveTimestamp = str(datetime.datetime.now())
            message = "Keep Alive Datalogger {0} \n\r".format(keepAliveTimestamp)
            print message
            time.sleep(10)

        except Exception as error:

            print "Error: ", error

if __name__ == "__main__":
    main()