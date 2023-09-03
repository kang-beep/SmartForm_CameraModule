import paho.mqtt.client as mqtt

class mqtt_send :
    
    def __init__(self, BROKER_NAME, TOPIC) -> None :
        self.BROKER_NAME = BROKER_NAME
        self.TOPIC = TOPIC
        self.client = mqtt.Client()
        self.client.on_connect = self.on_connect
        # self.client.on_message = self.on_message
        self.client.connect(self.BROKER_NAME, 1883, 60)
        

    def on_connect(self, client, userdata, flags, rc):
        print("Connected with result code "+str(rc))
        self.client.subscribe(self.TOPIC)

    # def on_message(self, client, userdata, msg):
        # print(f"Received message '{msg.payload}' on topic '{msg.topic}'")

    def send_on_message(self, byte_code):
        self.client.loop_start()
        self.client.publish(self.TOPIC, byte_code)
        self.client.loop_stop()

class mqtt_recv : 

    def __init__(self, BROKER_NAME, TOPIC) -> None:
        self.BROKER_NAME = BROKER_NAME
        self.TOPIC = TOPIC
        self.client = mqtt.Client()
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message
        

    def on_connect(self, client, userdata, flags, rc):
        print("Connected with result code "+str(rc))
        self.client.subscribe(self.TOPIC)

    def on_message(self, client, userdata, msg):
        print(f"Received message '{msg.payload}' on topic '{msg.topic}'")

    def signal_recv(self):
        self.client.connect(self.BROKER_NAME, 1883, 60)
        self.client.loop_forever()
