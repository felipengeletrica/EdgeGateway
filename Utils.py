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


import socket
from urllib import urlopen
import re


class Utils(object):

    @staticmethod
    def checkipformat(self, ip):

        try:

            regex = "^((25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\\.){3}(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$"
            mskformat = re.match(regex, ip)

            if mskformat:
                #ip = mskformat.group()
                return True
            else:
                return False
        except:
            raise

    @staticmethod
    def getlocalIp(self):

        """"Get local IP address.
        """
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(("8.8.8.8", 80))
            ip = s.getsockname()[0]
        except:
            ip = None
            raise

        finally:
            s.close()
            return ip

    @staticmethod
    def getPublicIp(self):

        """Get external IP using dyndns"""
        try:
            data = str(urlopen('http://checkip.dyndns.com/').read())
            #data = '<html><head><title>Current IP Check</title></head><body>Current IP Address: 65.96.168.198</body></html>\r\n'
            externalip = re.compile(r'Address: (\d+\.\d+\.\d+\.\d+)').search(data).group(1)

        except:
            externalip = None
            raise
        finally:
            return externalip

    @staticmethod
    def datafile(self, name, mode):

        try:
            data = open(name, mode)
        except:
            data = None

        return data

    @staticmethod
    def writedatafile(self, name, mode, message):

        try:
            with open(name, mode) as file:
                file.write(message)
        except:
            raise
