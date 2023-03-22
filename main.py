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
            devs.append(logger(devices[index]['description']))
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