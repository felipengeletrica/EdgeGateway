#!/usr/bin/env python3
# coding=utf-8
"""
MQTT Manager
"""

# region import
import threading
import time
import paho.mqtt.client as mqtt
import json

# endregion


class MqttManager(threading.Thread):
    def __init__(
        self,
        username: str,
        password: str,
        server: str,
        port: int,
        client: str,
        subscribe: str
    ):
        """
        Initialize MQTT Manager instance.

        :param username: MQTT broker username
        :type username: str
        :param password: MQTT broker password
        :type password: str
        :param server: MQTT broker server address
        :type server: str
        :param port: MQTT broker port
        :type port: int
        :param client: MQTT client identifier
        :type client: str
        :param subscribe: Topic to subscribe to
        :type subscribe: str
        """
        threading.Thread.__init__(self)
        self.server = server
        self.port = port
        self.client = mqtt.Client(client)
        self.__subscribe = subscribe
        self.client.username_pw_set(username=username, password=password)
        self.thread = threading.Thread(target=self._start)
        self.status = False
        self.retry = 3

    def _start(self):
        """
        Start process for MQTT manager.
        """
        print(f"Server: {self.server} Port: {self.port}")
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message

        while True:
            try:
                # Connect MQTT BROCKER
                mqttt_status = self.client.connect(host=self.server, port=self.port)
                if mqttt_status == 0:
                    self.status = True
                else:
                    self.status = False
                print("Running server")
                # Block loop
                self.client.loop_forever()

            except Exception as error:
                print(f"Fail Server: {self.server} Error:{error}")
                self.status = False
                # Add sleep in case down network
                time.sleep(0.3)
                pass

    def publish(self, topic, payload):
        """
        Publish message in broker.

        :param topic: Topic
        :type topic: str
        :param payload: Payload
        :type payload: str
        :return: Result code and message ID
        :rtype: tuple
        """

        (rc, mid) = (-1, -1)

        try:
            retry = self.retry
            while retry > 0:
                (rc, mid) = self.client.publish(topic=topic, payload=payload, qos=1)
                # print(f"Status publish: {(rc, mid)}")
                if rc == 0:
                    return rc
                time.sleep(0.3)
        except Exception as error:
            print(f"Fail publish error {error}")
        print("fail publish")
        return rc

    def on_connect(self, client, userdata, flags, rc):
        """
        The callback for when the client receives a CONNACK response from the server.

        :param client: Client
        :type client: paho.mqtt.client.Client
        :param userdata: Userdata
        :type userdata: object
        :param flags: Flags
        :type flags: dict
        :param rc: Result code
        :type rc: int
        """
        try:
            print(f"Connected with result code {str(rc)}")
            # Subscribing in on_connect() means that if we lose the connection and
            # reconnect then subscriptions will be renewed.
            client.subscribe(self.__subscribe)
        except Exception as error:
            print(f"Fail  on connect error {error}")

    def on_message(self, client, userdata, msg):
        """
        The callback for when a PUBLISH message is received from the server.

        :param client: Client
        :type client: paho.mqtt.client.Client
        :param userdata: User data
        :type userdata: object
        :param msg: Message
        :type msg: paho.mqtt.client.MQTTMessage
        """
        content = json.loads(msg.payload)
        # if self.on_message_callback:
        #     self.on_message_callback(content)  # Chama a função de callback com o conteúdo da mensagem

    def stop(self):
        """
        Stop the MQTT client.
        """
        print("Stop mqtt client")
        self.client.loop_stop()
        # self.thread.join()

    def run(self):
        """
        Run the MQTT manager.
        """
        self.thread.daemon = True
        self.thread.start()
