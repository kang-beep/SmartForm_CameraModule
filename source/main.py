import RPi.GPIO as GPIO
import device_module
import mqtt_handler
import threading

def run():
    GPIO.setmode(GPIO.BCM)
    print("모듈 구동")

    # pin할당
    _collusion = device_module.collusion(18, 21)
    _motor = device_module.motor(IN1=17, IN2=27, IN3=22, IN4=23)
    _camera = device_module.CameraControl("/home/sks/Desktop/camera_module/image")

    # mqtt 활성화
    _mqtt_send = mqtt_handler.mqtt_send(BROKER_NAME = "broker.hivemq.com", TOPIC="f8oCa2e7FJc1")

    # recv 토픽 바꿀것
    _mqtt_recv = mqtt_handler.mqtt_recv(BROKER_NAME = "broker.hivemq.com", TOPIC="f8oCa2e7FJc1")

    direction_status = True
    try :

            # 모터 정방향 회전
            while direction_status == True : 
                _motor.step_motor_rotate()
                if GPIO.input(_collusion.end_pin) == GPIO.LOW :
                    direction_status = False
                    break

            # 모터 역방향 회전
            while direction_status == False:     
                _motor.step_motor_rotate_reverse()
                if GPIO.input(_collusion.start_pin) == GPIO.LOW :
                    direction_status = True
                    break
            
            # 정위치 제자리
            for i in range(50):
                _motor.step_motor_rotate_reverse()

    except KeyboardInterrupt :
        GPIO.cleanup(0)

if __name__ == "__main__" : # 다른 python 파일에서 import를 할때, 이 코드는 실행되지않음( 모듈의 독립성,가독성 유지 )
    run()
    