import RPi.GPIO as GPIO
import device_module
import mqtt_handler

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
    try :
        while True:
            if GPIO.input(_collusion.end_pin) == GPIO.HIGH :
                # 모터 정방향 회전
                _motor.step_motor_rotate()
                
            else :
                # 모터 역방향 회전
                _motor.step_motor_rotate_reverse()
                
                # 10초마다 사진 촬영 코드 작성
                _camera.camActivate()

                # 촬영된 이미지 바이트 코드로 변환후 전송
                byte_code = _camera.image_to_byte()
                _mqtt_send.send_image(byte_code)

                
    except KeyboardInterrupt :
        GPIO.cleanup(0)

if __name__ == "__main__" : # 다른 python 파일에서 import를 할때, 이 코드는 실행되지않음( 모듈의 독립성,가독성 유지 )
    run()
    