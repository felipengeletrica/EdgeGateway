#!/usr/bin/env python
#-*- coding: latin-1 -*-

import sys
import os
import datetime


debug = False

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
script_path = os.path.dirname(os.path.abspath(__file__))

import Utils


class DataAnalysis(object):

    def __init__(self):

        try:
            print "Data Analysis init"

        except Exception as error:
            raise error

    def processdata(self, data, description):

        try:
            #save in CSV format
            timestamp = str(datetime.datetime.now())
            dataforsave = "{0};{1};{2}\r".format(description, data, timestamp)
            Utils.Utils.writedatafile("logs.csv", 'a', dataforsave)
            print dataforsave

        except Exception as error:
            raise error
