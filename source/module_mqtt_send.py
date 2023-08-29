import paho.mqtt.client as mqtt

class MQTT_send :
    
    def __init__(self, mqtt_broker_name, mqtt_topic) -> None :

        self.mqtt_broker_name = mqtt_broker_name
        self.mqtt_topic = mqtt_topic
        self.client = mqtt.Client()
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message
        self.client.connect("broker.hivemq.com", 1883, 60)
        self.client.loop_start()

    def on_connect(self, client, userdata, flags, rc):
        print("Connected with result code "+str(rc))
        client.subscribe("f8oCa2e7FJc1")

    def on_message(self, client, userdata, msg):
        print(f"Received message '{msg.payload.decode()}' on topic '{msg.topic}'")

    def send_image(self):
        while True :
            message = input("Enter a message to send: ")
            print()
            self.client.publish("f8oCa2e7FJc1", message)