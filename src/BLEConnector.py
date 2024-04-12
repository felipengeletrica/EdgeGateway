import threading
from bluepy.btle import Scanner, DefaultDelegate

class BLEConnector(threading.Thread):
    def __init__(self, device_name):
        self.device_name = device_name
        self.service_uuid = None
        self.characteristic_uuid = None
    def run(self, service_uuid, characteristic_uuid):
        self.service_uuid = service_uuid
        self.characteristic_uuid = characteristic_uuid
        self._process = p = threading.Thread(target=self._process)
        p.daemon = True
        p.start()

    def _process(self):

        while True:
            try:
                device = self.scan_devices()
                if not device:
                    continue
                try:
                    device.connect()
                    services = device.getServices()
                    for service in services:
                        if service.uuid == self.service_uuid:
                            characteristics = service.getCharacteristics()
                            for char in characteristics:
                                if char.uuid == self.characteristic_uuid:
                                    data = char.read()
                                    print(data)
                    continue
                except Exception as e:
                    return None, str(e)
