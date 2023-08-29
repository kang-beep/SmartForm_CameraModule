import paho.mqtt.client as mqtt


class MQTT_recv : 

    def __init__(self, mqtt_broker_name, mqtt_topic) -> None:
        self.mqtt_broker_name = mqtt_broker_name
        self.mqtt_topic = mqtt_topic
        self.client = mqtt.Client()
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message
        self.client.connect("broker.hivemq.com", 1833, 60)
        
    def on_connect(client, userdata, flags, rc):
        print("Connected with result code "+str(rc))
        client.subscribe("f8oCa2e7FJc1")

    def on_message(client, userdata, msg):
        print(f"Received message '{msg.payload.decode()}' on topic '{msg.topic}'")

    def recv_signal_message(self):
        self.client.loop_forever()
