
import RPi.GPIO as GPIO
import threading
import mqtt_handler
import device_module
import time
# 1. 모터 정방향, 역방향 테스트
# 2. 충돌 센서 테스트
# 3. 카메라 사진 테스트
# 4. mqtt sender, reciver 테스트

def motor_test(): 
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    _motor = device_module.motor(17,27,22,23)

    try :
        while True: 
            # _motor.step_motor_rotate()

            _motor.step_motor_rotate_reverse()

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

    _camera = device_module.CameraControl("/home/sks/Desktop/camera_module/image")
    
    bytes_image = _camera.image_to_byte(_camera.IMAGE_PATH)
    print(bytes_image)

def image_to_byte(image_path):
        with open(image_path, 'rb') as image_file:
            return image_file.read()

def byte_to_image(byte_data, output_path):
    with open(output_path, 'wb') as output_file:
        output_file.write(byte_data)

def on_message(self, client, userdata, msg):
    byte_to_image(msg.payload, "/home/sks/Desktop/camera_module/test_image/output_image.png")


_mqtt_recv = mqtt_handler.mqtt_recv(BROKER_NAME = "broker.hivemq.com", TOPIC="f8oCa2e7FJc1")
_mqtt_recv.on_message = on_message

#_mqtt_recv = mqtt_handler.mqtt_recv(BROKER_NAME="broker.hivemq.com", TOPIC="f8oCa2e7FJc1")
#_mqtt_recv.on_message = on_message
# output_image_path = "/home/sks/Desktop/camera_module/test_image/output_image.png"
# byte_to_image(byte_data, output_image_path)






