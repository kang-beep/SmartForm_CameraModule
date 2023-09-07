import os
import paho.mqtt.client as mqtt
import datetime
def run():
        # logger.info(f"sub thread start {threading.currentThread().getName()}")
        absolute_path = os.path.join("/home/sks/Desktop/camera_module/static")
        path = absolute_path
        # logger.info(path)

        global count
        count = 0 

        # connect_to = MongoClient("mongodb://smartfarm:acin*0446@203.252.230.243:27017/")

        # collection = mdb.test_data_images
        # collection2 = mdb.test_data_images_date # 이미지 날짜  

        now_date = None # 날짜

        def on_connect(client, userdata, flags, rc):
            if rc == 0:
                # logger.info("이미지 리시버가 클라이언트와 연결 되었습니다.")
                print("이미지 리시버가 클라이언트와 연결 되었습니다.")
            else:
                # logger.info(f"Bad connection Returned code={rc}")
                print(f"Bad connection Returned code={rc}")


        def on_disconnect(client, userdata, flags, rc=0):
            # logger.info("이미지 리시버가 클라이언트와 해제 되었습니다.")
            print("이미지 리시버가 클라이언트와 해제 되었습니다.")
            client.loop_stop()
            client.loop_start()


        def on_subscribe(client, userdata, mid, granted_qos):
            # logger.info(f"연결 상태 : {str(mid)} {str(granted_qos)}")
            print(f"연결 상태 : {str(mid)} {str(granted_qos)}")


        def on_message(client, userdata, msg):
            global count, now_date, now_db_date
            if str(msg.payload) == "b'directory_create'":
                now = datetime.datetime.now()
                now_date = now.strftime('%Y-%m-%d_%H_%M')
                now_db_date = now.strptime(now_date,'%Y-%m-%d_%H_%M')
                os.mkdir(f"{path}{now_date}")
                # logger.info("이미지 폴더 생성")
                print("이미지 폴더 생성 ")
            elif str(msg.payload) == "b'last_img'":
                count = 0
                # logger.info("마지막 이미지 생성")
                print("마지막 이미지 생성")
            else:
                # 클라이언트에서 받아온 값을 디코딩 
                # cv2.imwrite("./out.jpg", msg)
                # logger.info("이미지 생성")
                print("이미지 생성")
                with open(f'{path}{now_date}/output_{count}.jpg', "wb") as f:
                    f.write(msg.payload)
                print(f"Image Received {count}")
                count += 1
                    
        # 새로운 클라이언트 생성
        client = mqtt.Client(client_id = "pc_receive", clean_session= True)

        # 콜백 함수
        client.on_connect = on_connect
        client.on_disconnect = on_disconnect
        client.on_subscribe = on_subscribe
        client.on_message = on_message

        client.connect('broker.hivemq.com', 1883, 60)

        client.subscribe("f8oCa2e7FJc2")
        
        client.loop_forever()

run()
        
