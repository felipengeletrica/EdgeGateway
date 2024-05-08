import threading
import time
import bluetooth
import pynmea2
from src.storage.Dataanalysis import DataAnalysis

class BluetoothGpsAgrinavi(threading.Thread):

    def __init__(self, description: str, timeIgnoreData=1):

        self.description = description
        self.address = None
        self.port = None
        self.socket_buffer = 4096
        self.gps_time_ignore_data = timeIgnoreData
        self.__start_time = time.time() + timeIgnoreData
        self.dataanalysis = DataAnalysis()

    def run(self, port, address):

        self.port = port
        self.address = address
        self._process = p = threading.Thread(target=self._process)
        p.daemon = True
        p.start()

    def __process_data(self, data):

        data_str = str(data)

        lines = data_str.split("\\r\\n")
        for line in lines:
            try:
                msg = pynmea2.parse(line)
                self.dataanalysis.processdata(str(msg), self.description)
            except:
                continue
        return

    def _process(self):

        first_execution = False
        while True:
            try:
                # create a socket and connect to it.
                socket = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
                socket.connect((self.address, self.port))

                while True:
                    time_now = time.time()

                    data = socket.recv(self.socket_buffer)
                    if time_now > self.__start_time or first_execution is False:
                        first_execution = True
                        self.__start_time = time_now + self.gps_time_ignore_data
                        if data:
                            self.__process_data(data=data)
                    time.sleep(0.01)
            except Exception as err:
                print(f"[ Error ] - {err}")
                time.sleep(1)
