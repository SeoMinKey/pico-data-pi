from machine import Pin, PWM
import time

# ---- 부저를 PWM 모드로 설정 (GP22) ----
buzzer = PWM(Pin(22))

# ---- 음과 소리크기 설정 ----
buzzer.freq(440)        # 주파수 440Hz = 음

while True:
    buzzer.duty_u16(30000)  # 볼륨 켜기 (0 ~ 65535 중간값 정도)  
    time.sleep(1)           # 1초 동안 유지
    buzzer.duty_u16(0)      # 볼륨 끄기
    time.sleep(1)           # 1초 동안 유지