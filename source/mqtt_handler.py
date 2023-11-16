import paho.mqtt.client as mqtt
import socket, time

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
        self.client.on_disconnect = self.on_disconnect
        self.client.on_message = self.on_message
        
        
    def on_connect(self, client, userdata, flags, rc):
        print("Connected with result code "+str(rc))
        self.client.subscribe(self.TOPIC)

    def on_disconnect(self, client, userdata, flags, rc=0):
        print(str(rc))
        print("------------")
        network_check()
        self.client.reconnect()

    def on_message(self, client, userdata, msg):
        print(f"Received message '{msg.payload}' on topic '{msg.topic}'")

    def signal_recv_start(self):
        self.client.connect(self.BROKER_NAME, 1883, 60)
        self.client.loop_forever()


def network_check():
    while True:
            
            ipaddress=socket.gethostbyname(socket.gethostname())
            if ipaddress=="127.0.0.1":
                print("You are not connected to the internet!")
            else:
                print("You are connected to the internet with the IP address of "+ ipaddress )
                break
            time.sleep(5)
