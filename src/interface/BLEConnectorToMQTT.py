import threading
import json
import datetime
from bluepy.btle import UUID, Peripheral, DefaultDelegate
from queue import Queue
from src.interface.mqtt_manager import MqttManager
import logging

# Configure logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(levelname)s %(message)s')
logger = logging.getLogger(__name__)

debug = False

# UUIDs
SERVICE_UUID = "4fafc201-1fb5-459e-8fcc-c5c9c331914b"
CHARACTERISTIC_UUID = "beb5483e-36e1-4688-b7f5-ea07361b26a8"
# BLE BUFFER
BLE_BUFFER = 2048


class DelegateBT(DefaultDelegate):
    def __init__(self, data_queue):
        super().__init__()
        self.data_queue = data_queue

    def handleNotification(self, cHandle, data):
        self.data_queue.put(data)


class BLEConnectorToMQTT(threading.Thread):
    def __init__(self, device_name, server_mqtt, timeout):
        threading.Thread.__init__(self)
        self.device_name = device_name
        self.service_uuid = SERVICE_UUID
        self.characteristic_uuid = CHARACTERISTIC_UUID
        self.mac_address = None
        self.timeout = timeout

        self.mqtt_manager = MqttManager(
            username=server_mqtt['username'],
            password=server_mqtt['password'],
            server=server_mqtt['server'],
            port=server_mqtt['port'],
            client='client1',
            subscribe_upstream=server_mqtt['subscribe-upstream'],
            subscribe_downstream=server_mqtt['subscribe-downstream'],
            on_message_callback=self.senddata
        )

        self.subscribe_upstream = server_mqtt['subscribe-upstream']
        self.subscribe_downstream = server_mqtt['subscribe-downstream']
        self.data_queue = Queue()

    def run(self, mac_address):
        self.mac_address = mac_address
        self.mqtt_manager.run()
        self._process = threading.Thread(target=self._process)
        self._process.daemon = True
        self._process.start()
        self._data_processor = threading.Thread(target=self._process_data)
        self._data_processor.daemon = True
        self._data_processor.start()

    def _process(self):
        while True:
            try:
                logger.info("MAC: " + self.mac_address)
                peripheral = Peripheral(self.mac_address)
                peripheral.setDelegate(DelegateBT(self.data_queue))

                # Set MTU size
                peripheral.setMTU(BLE_BUFFER)

                service = peripheral.getServiceByUUID(UUID(self.service_uuid))
                characteristic = service.getCharacteristics(UUID(self.characteristic_uuid))[0]

                # Enable notifications
                peripheral.writeCharacteristic(characteristic.getHandle() + 1, b"\x01\x00", withResponse=True)

                while True:
                    if peripheral.waitForNotifications(self.timeout):
                        continue
            except Exception as e:
                logger.error(f"Error in _process: {e}")
            finally:
                try:
                    peripheral.disconnect()
                except Exception as e:
                    logger.error(f"Error disconnecting: {e}")

    def _process_data(self):
        while True:
            data = self.data_queue.get()
            self.handle_data(data)

    def handle_data(self, data):
        try:
            # First verification json
            if len(data) and "{" in data.decode() and ":" in data.decode():
                try:
                    logger.debug(f'raw: {data}')
                    json_obj = json.loads(data.decode())
                    metadata = {"timestamp": str(datetime.datetime.now())}
                    payload = {"gateway_meta": metadata, "data": json_obj}
                    payload_dumps = json.dumps(payload)
                    self.mqtt_manager.publish(self.subscribe_upstream, payload_dumps)
                    if debug:
                        logger.debug(f'{payload_dumps} [{str(datetime.datetime.now())}]')
                except json.JSONDecodeError:
                    logger.warning("Invalid json")
        except Exception as error:
            logger.exception(f"exception data: {error}")

    def senddata(self, message_content):
        try:
            if self.serialstate():
                try:
                    if isinstance(message_content, dict):
                        if 'raw' in message_content:
                            raw_value = message_content.get("raw")
                            self.s.write(raw_value.encode())
                            logger.info(f"Message RAW via serial: {raw_value}")
                        else:
                            message_json = json.dumps(message_content)
                            self.s.write(message_json.encode())
                            logger.info("Sent via serial: %s", message_content)
                    else:
                        logger.warning("message_content is not a dictionary.")
                except Exception as error:
                    logger.exception("Error sending data via serial: %s", error)
            else:
                logger.warning("Serial connection is not open.")
        except Exception as error:
            logger.exception("Error sending data via serial: %s", error)
