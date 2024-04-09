#!/usr/bin/env python
#-*- coding: latin-1 -*-

import sys
import os
import datetime
from pynmeagps import NMEAReader


debug = False

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
script_path = os.path.dirname(os.path.abspath(__file__))
parent_path = os.path.abspath(os.path.join(script_path, os.pardir))

import Utils


class DataAnalysis(object):

    def __init__(self):
        self.created_at = datetime.datetime.now().strftime('%H-%M-%S')
        try:
            print("Data Analysis init")

        except Exception as error:
            raise error

    def processdata(self, data, description):
        #save in CSV format
        try:
            print(description)
            file_server_dir = os.path.join(parent_path, "file-server")
            if not os.path.exists(file_server_dir):
                os.makedirs(file_server_dir)

            # create folder "logs"
            logs_dir = os.path.join(file_server_dir, "logs")
            if not os.path.exists(logs_dir):
                os.makedirs(logs_dir)

            # create <description_log_dir>
            folder = description.lower().replace(' ', '-')
            description_log_dir = os.path.join(logs_dir, folder)
            if not os.path.exists(description_log_dir):
                os.makedirs(description_log_dir)

            # get date and hour in specific format
            now = datetime.datetime.now()
            hour = now.strftime('%H:%M:%S')
            date = now.strftime('%Y-%m-%d')

            # define filename
            filename = f"{date}_{self.created_at}.csv"

            # final filepath
            filepath = os.path.join(description_log_dir, filename)

            # content
            dataforsave = f"{data};{hour}\r\n"
            print(dataforsave)

            msg = NMEAReader.parse(f'{data}\r\n')
            print(msg)

            # save data
            Utils.Utils.writedatafile(filepath, 'a', dataforsave)

        except Exception as error:
            raise error
