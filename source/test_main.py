import time
import os
import RPi.GPIO as GPIO
import device_module
import mqtt_handler

def run():
    GPIO.setmode(GPIO.BCM)
    print("모듈 구동")

    # pin할당
    _collusion = device_module.collusion(18, 21)
    _motor = device_module.motor(IN1=17, IN2=27, IN3=22, IN4=23)

    # 카메라 인스턴스 생성
    absolute_path = os.path.join("/home/sks/Desktop/camera_module/image", "image.jpg")
    _camera = device_module.CameraControl(absolute_path)


    # recv 토픽 바꿀것
    _mqtt_send = mqtt_handler.mqtt_send(BROKER_NAME = "broker.hivemq.com", TOPIC="f8oCa2e7FJc2")
    
    direction_status = True
    try :

        # 모터 정방향 회전 
        while direction_status == True :
            _motor.step_motor_rotate()
            if GPIO.input(_collusion.end_pin) == GPIO.LOW :
                direction_status = False

        # 모터 역방향 회전
        start_time = time.time()

        # 폴더 생성 신호 보내기
        _mqtt_send.send_on_message(byte_code= "directory_create")

        while direction_status == False:
            
            _motor.step_motor_rotate_reverse()
            if GPIO.input(_collusion.start_pin) == GPIO.LOW :
                _mqtt_send.send_on_message(byte_code= "last_img")
                direction_status = True

            elif (time.time() - start_time) > 15 :
                start_time = time.time()
                print("사진찍기")
                # 사진 찍기
                _camera.camActivate()
                # 이미지 바이트 코드로 변환
                byte_image = _camera.image_to_byte()
                # 변환된 이미지 전송
                _mqtt_send.send_on_message(byte_code= byte_image)

        for i in range(50):
            _motor.step_motor_rotate()

    except KeyboardInterrupt :
        print("강제 종료")
        _camera.camera.close()
        GPIO.cleanup(0)
    
    except Exception as e :
        print("에러 코드", e)
        _camera.camera.close()
        GPIO.cleanup(0)

    finally : 
        # 무슨일이 있어도 핀과 카메라는 종료시 메모리 할당을 해제해 줘야 됩니다.
        _camera.camera.close()
        GPIO.cleanup(0)

# recv mqtt on_message modify
def recv_on_message(client, userdata, msg):
    print(msg.payload)

    if str(msg.payload) == "b'camera_start'" :
        run()
        # pin = 18
        # pin_status = GPIO.gpio_function(pin)
        # if pin_status != GPIO.IN:
        #     print("핀이 할당 되지 않았습니다. 초기화 진행")
        #     run()
        # else :
        #     print("핀이 할당된 상태입니다. 계속 진행")
        


if __name__ == "__main__" : # 다른 python 파일에서 import를 할때, 이 코드는 실행되지않음( 모듈의 독립성,가독성 유지 )

    # mqtt 활성화
    _mqtt_recv = mqtt_handler.mqtt_recv(BROKER_NAME = "broker.hivemq.com", TOPIC="f8oCa2e7FJc1")

    # on_message 함수를 외부에서 재정의
    _mqtt_recv.client.on_message = recv_on_message
    
    # 통신시작
    _mqtt_recv.signal_recv_start()
    
    