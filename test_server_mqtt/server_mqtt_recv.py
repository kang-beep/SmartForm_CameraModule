import paho.mqtt.client as mqtt

class recv :

    def __init__(self) -> None:
        pass

    def on_connect(self, client, userdata, flags, rc):
        if rc == 0: 
            print("connect OK")
        else :
            print("Bad connection Returned code=", rc)

    def on_disconnect(self, client, userdata, flags, rc):
        print(str(rc))

    def on_publish(self, client, userdata, mid):
        print("In on_hub callback mid= ", mid)

    def recv_message(self):
        broker = "broker.hivemq.com"
        port = 1883
        # 새로운 클라이언트 생성
        client = mqtt.Client()
        # 콜백 함수 설정 on_connect(브로커에 접속)
        # on_disconnect(브로커에 접속종료)
        # on_publish(메세지 발행)
        client.on_connect = on_connect
        client.on_disconnect = on_disconnect
        client.on_publish = on_publish
        # address : Localhost, port: 1883 에 연결
        client.connect('localhost', 1883)

        client.loop_forever()
        # common topic 으로 메세지 발행
        
        