import RPi.GPIO as GPIO
import threading
import time

import device_module
import mqtt_handler

def run():
    GPIO.setmode(GPIO.BCM)
    print("모듈 구동")

    # pin할당
    _collusion = device_module.collusion(18, 21)
    _motor = device_module.motor(IN1=17, IN2=27, IN3=22, IN4=23)
    _camera = device_module.CameraControl("/home/sks/Desktop/camera_module/image")


    # recv 토픽 바꿀것
    _mqtt_send = mqtt_handler.mqtt_send(BROKER_NAME = "broker.hivemq.com", TOPIC="f8oCa2e7FJc2")

    direction_status = True
    try :
        while True:

            # 모터 역방향 회전
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

                elif (time.time() - start_time) > 10 :
                    start_time = time.time()
                    # 사진 찍기
                    # _camera.camActivate
                    # 이미지 바이트 코드로 변환
                    # byte_image = _camera.image_to_byte
                    # 변환된 이미지 전송
                    # _mqtt_send.send_on_message(byte_code= byte_image)
                
    except KeyboardInterrupt :
        GPIO.cleanup(0)


# on_message overRiding modify
def on_message(client, userdata, msg):
    if str(msg.payload) == "'b'camera_start" :
        run()
    

if __name__ == "__main__" : # 다른 python 파일에서 import를 할때, 이 코드는 실행되지않음( 모듈의 독립성,가독성 유지 )

    # mqtt 활성화
    _mqtt_recv = mqtt_handler.mqtt_recv(BROKER_NAME = "broker.hivemq.com", TOPIC="f8oCa2e7FJc1")
    _mqtt_recv.on_message = on_message
    _mqtt_recv.signal_recv()
    
    