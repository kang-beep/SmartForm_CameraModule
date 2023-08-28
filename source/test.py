import device_module

# 1. 모터 정방향, 역방향 테스트
# 2. 충돌 센서 테스트
# 3. 카메라 사진 테스트
# 4. mqtt sender, reciver 테스트

def motor_test(): 
    _motor = device_module.motor(17,22,27,23)

    for i in range(0,5): 
        _motor.step_motor_rotate()

def collusion():
    _collusion = device_module.collusion(4, 21)
    
    if


