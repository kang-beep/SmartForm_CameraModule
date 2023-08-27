import RPi.GPIO as GPIO
import module


def run():
    GPIO.setmode(GPIO.BCM)
    print("모듈 구동")

    # pin할당
    _collusion = module.collusion(21, 2)
    _motor = module.motor(IN1=17, IN2=27, IN3=22, IN4=23)
    _camera = module.camera()

    try :
        while True:
            if GPIO.input(_collusion.start_crash_pin) == GPIO.HIGH :
                # 모터 정방향 회전
                
            else :
                # 모터 역방향 회전
                

                

    except KeyboardInterrupt :

if __name__ == "__name__" : # 다른 python 파일에서 import를 할때, 이 코드는 실행되지않음( 모듈의 독립성,가독성 유지 )
    run()