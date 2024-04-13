from bluepy.btle import UUID, Peripheral, DefaultDelegate

# UUIDs
SERVICE_UUID = "4fafc201-1fb5-459e-8fcc-c5c9c331914b"
CHARACTERISTIC_UUID = "beb5483e-36e1-4688-b7f5-ea07361b26a8"

class MyDelegate(DefaultDelegate):
    def __init__(self, params):
        DefaultDelegate.__init__(self)

    def handleNotification(self, cHandle, data):
        print("Received data: {}".format(data.decode()))

# Connect to the BLE device
peripheral = Peripheral("58:BF:25:16:D0:62")
peripheral.setDelegate(MyDelegate(None))

# Find the service and characteristic
service = peripheral.getServiceByUUID(UUID(SERVICE_UUID))
characteristic = service.getCharacteristics(UUID(CHARACTERISTIC_UUID))[0]

# Enable notifications
peripheral.writeCharacteristic(characteristic.valHandle + 1, b"\x01\x00", withResponse=True)

try:
    while True:
        if peripheral.waitForNotifications(1.0):
            continue
finally:
    peripheral.disconnect()
