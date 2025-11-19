from machine import Pin
import time

# ---- 버튼 핀 설정 ----
button = Pin(20, Pin.IN, Pin.PULL_UP) # PULL_UP 모드

while True:
    if button.value() == 0:      # 누르면 0
        print("버튼 눌림")
    
    time.sleep(0.2)              # 0.2초마다 체크