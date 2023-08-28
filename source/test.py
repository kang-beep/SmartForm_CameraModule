import device_module
import RPi.GPIO as GPIO
# 1. 모터 정방향, 역방향 테스트
# 2. 충돌 센서 테스트
# 3. 카메라 사진 테스트
# 4. mqtt sender, reciver 테스트

def motor_test(): 
    _motor = device_module.motor(17,27,22,23)

    try :
        for i in range(0,5): 
            _motor.step_motor_rotate()
    except KeyboardInterrupt :
        GPIO.cleanup(0)
        exit(0)

def collusion():
    _collusion = device_module.collusion(18, 21)
    
    try :
        while True:
            if GPIO.input(_collusion.start_pin) == GPIO.LOW :
                # 모터 정방향 회전
                print("start of rail")
                
            elif GPIO.input(_collusion.end_pin) == GPIO.LOW :
                # 모터 역방향 회전
                print("end of rail")
    except KeyboardInterrupt :
        GPIO.cleanup(0)
        exit(0)

def camera():

    _camera = device_module.CameraControl
    
    _camera.camActivate()
    


