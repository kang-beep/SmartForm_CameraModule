from picamera import PiCamera as cam
import RPi.GPIO as GPIO
import time

class collusion():

    def __init__(self, START_PIN, END_PIN) -> None:
        self.start_pin = START_PIN
        self.end_pin = END_PIN
        
        GPIO.setup(START_PIN, GPIO.IN)
        GPIO.setup(END_PIN, GPIO.IN)


class motor():
    
    def __init__(self, IN1, IN2, IN3, IN4) -> None:
        
        self.IN1 = IN1
        self.IN2 = IN2
        self.IN3 = IN3
        self.IN4 = IN4

        GPIO.setup(IN1, GPIO.OUT)
        GPIO.setup(IN2, GPIO.OUT)
        GPIO.setup(IN3, GPIO.OUT)
        GPIO.setup(IN4, GPIO.OUT)


        self.steps_per_rotation = 512  # 1회전에 필요한 스텝 수
        self.delay = 0.001   # 회전 딜레이 (딜레이없이 움직이면 모터가 불안정해짐)

        # 시퀸스 정의
        self.step_sequence = [
            [1, 0, 0, 0],
            [1, 1, 0, 0],
            [0, 1, 0, 0],
            [0, 1, 1, 0],
            [0, 0, 1, 0],
            [0, 0, 1, 1],
            [0, 0, 0, 1],
            [1, 0, 0, 1]
        ]
        # 역방향 시퀸스
        self.reversed_sequence = self.step_sequence[::-1]

        # 스텝 카운트
        self.step_count = len(self.step_sequence)
        

    # 스텝모터 회전 함수
    def step_motor_rotate(self):
        
        for step in range(self.step_count):
            GPIO.output(self.IN1, self.step_sequence[step][0])
            GPIO.output(self.IN2, self.step_sequence[step][1])
            GPIO.output(self.IN3, self.step_sequence[step][2])
            GPIO.output(self.IN4, self.step_sequence[step][3])
            time.sleep(self.delay)
    
    def step_motor_rotate_reverse(self):
        
        for step in range(self.step_count):
            GPIO.output(self.IN1, self.reversed_sequence[step][0])
            GPIO.output(self.IN2, self.reversed_sequence[step][1])
            GPIO.output(self.IN3, self.reversed_sequence[step][2])
            GPIO.output(self.IN4, self.reversed_sequence[step][3])
            time.sleep(self.delay)
        
class CameraControl:
    
    def __init__(self, IMAGE_PATH):
        # 카메라 초기화
        self.camera = cam()
        self.IMAGE_PATH = IMAGE_PATH

        # 카메라 해상도 설정(옵션)
        self.camera.resolution = (640, 640)

    def camActivate(self) :
        # 카메라 캡처
        self.camera.capture(self.IMAGE_PATH)

        
    def image_to_byte(self):
        with open(self.IMAGE_PATH, 'rb') as image_file:
            return image_file.read()

