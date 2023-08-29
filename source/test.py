import device_module
import RPi.GPIO as GPIO
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
            for i in range (1000):
                _motor.step_motor_rotate()

            time.sleep(2)

            for i in range (5):
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

    _camera = device_module.CameraControl
    
    _camera.camActivate()


collusion()
