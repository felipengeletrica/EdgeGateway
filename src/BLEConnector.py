import threading
from bluepy.btle import UUID, Peripheral, DefaultDelegate


# UUIDs
SERVICE_UUID = "4fafc201-1fb5-459e-8fcc-c5c9c331914b"
CHARACTERISTIC_UUID = "beb5483e-36e1-4688-b7f5-ea07361b26a8"


class DelegateBT(DefaultDelegate):
    def __init__(self, params):
        DefaultDelegate.__init__(self)

    def handleNotification(self, cHandle, data):
        print("Received data: {}".format(data.decode()))


class BLEConnector(threading.Thread):
    def __init__(self, device_name):
        self.device_name = device_name
        self.service_uuid = SERVICE_UUID
        self.characteristic_uuid = CHARACTERISTIC_UUID
        self.mac_address = None

    def run(self, mac_address):
        self.mac_address = mac_address
        self._process = p = threading.Thread(target=self._process)
        p.daemon = True
        p.start()

    def _process(self):

        while True:
            # Connect to the BLE device
            print("MAC: " + self.mac_address)
            peripheral = Peripheral(self.mac_address)
            peripheral.setDelegate(DelegateBT(None))

            # Find the service and characteristic
            service = peripheral.getServiceByUUID(UUID(self.service_uuid))
            characteristic = service.getCharacteristics(UUID(self.characteristic_uuid))[0]

            # Enable notifications
            peripheral.writeCharacteristic(characteristic.valHandle + 1, b"\x01\x00", withResponse=True)

            try:
                while True:
                    if peripheral.waitForNotifications(1.0):
                        continue
            finally:
                peripheral.disconnect()

      