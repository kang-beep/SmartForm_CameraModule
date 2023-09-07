import RPi.GPIO as GPIO
import threading
import mqtt_handler
import device_module
import time
import os

# 1. 모터 정방향, 역방향 테스트
# 2. 충돌 센서 테스트
# 3. 카메라 사진 테스트
# 4. mqtt sender, reciver 테스트

def motor_test(): 
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    _motor = device_module.motor(17,27,22,23)
    _collusion = device_module.collusion(18, 21)


    direction_status = True
    try :
        while True:
            # 모터 정방향 회전 
            while direction_status == True : 
                _motor.step_motor_rotate()
                if GPIO.input(_collusion.end_pin) == GPIO.LOW :
                    direction_status = False
                    break

            # 모터 역방향 회전
            start_time = time.time()
            
            while direction_status == False:   
                _motor.step_motor_rotate_reverse()
                if GPIO.input(_collusion.start_pin) == GPIO.LOW :
                    direction_status = True
                    break

    except KeyboardInterrupt :
        GPIO.cleanup(0)
        exit(0)

def collusion():
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    _collusion = device_module.collusion(18, 21)
    
    try :
        while True:
            if GPIO.input(_collusion.start_pin) == GPIO.LOW :
                print("start of rail")
                
            elif GPIO.input(_collusion.end_pin) == GPIO.LOW :
                print("end of rail")
    except KeyboardInterrupt :
        GPIO.cleanup(0)
        exit(0)

def camera():
    
    try : 
        absolute_path = os.path.join("/home/sks/Desktop/camera_module/image", "image.jpg")
        _camera = device_module.CameraControl(absolute_path)
        while True: 
            time.sleep(3)
            _camera.camActivate()
            print("사진찍기 완료")
            bytes_image = _camera.image_to_byte()
            print(bytes_image)
            
        _camera.close()
    except Exception as e :
        _camera.close()
        print("사진 찍기 에러", e)
        

def image_to_byte(image_path):
    with open(image_path, 'rb') as image_file:
        return image_file.read()

def byte_to_image(byte_data, output_path):
    with open(output_path, 'wb') as output_file:
        output_file.write(byte_data)

def on_message(client, userdata, msg):
    print(f"Received message '{msg.payload}' on topic '{msg.topic}'")
    return byte_to_image(msg.payload, "/home/sks/Desktop/camera_module/test_image/output_image.png")

def timer_function():
    # 타이머를 실행할 동작
    print("10 seconds have passed!")

# print(os.path.exists("/home/sks/Desktop/camera_module/image") )
# print(os.getcwd())
absolute_path = os.path.join("/home/sks/Desktop/camera_module/image", "image.jpg")
_camera = device_module.CameraControl(absolute_path)
_mqtt_send = mqtt_handler.mqtt_send(BROKER_NAME = "broker.hivemq.com", TOPIC="f8oCa2e7FJc2")

for i in range(5):
    _camera.camActivate()
    _camera.image_to_byte()
    _mqtt_send.send_on_message()

_camera.camera.close()



# time.sleep(2)


# start_time = time.time()
# while True:
#     if (time.time() - start_time) > 3 :
#         start_time = time.time()
#         print("3 seconds have passed!")
#         time.sleep(2)
    
#     time.sleep(1)
#     print("nothing")

#_mqtt_recv = mqtt_handler.mqtt_recv(BROKER_NAME = "broker.hivemq.com", TOPIC="f8oCa2e7FJc1")
#_mqtt_recv.client.on_message = on_message

#_mqtt_recv.signal_recv()

#_mqtt_recv = mqtt_handler.mqtt_recv(BROKER_NAME="broker.hivemq.com", TOPIC="f8oCa2e7FJc1")
#_mqtt_recv.on_message = on_message
# output_image_path = "/home/sks/Desktop/camera_module/test_image/output_image.png"
# byte_to_image(byte_data, output_image_path)






