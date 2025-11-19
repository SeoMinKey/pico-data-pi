from machine import Pin, I2C
import time
import ssd1306

# I2C 설정 (SCL=5, SDA=4)
i2c = I2C(0, scl=Pin(5), sda=Pin(4))

# OLED 128x64 설정
oled = ssd1306.SSD1306_I2C(128, 64, i2c)

text = "Hello"
x = 0
y = 20        # 화면 중앙-ish
dx = 2        # 이동 속도 (픽셀 단위)

while True:
    oled.fill(0)          # 화면 지우기
    oled.text(text, x, y) # 글자 그리기
    oled.show()           # 업데이트

    x += dx               # 위치 이동

    # 화면 밖으로 나가면 방향 반전
    if x <= 0 or x >= (128 - len(text)*8):
        dx = -dx

    time.sleep(0.05)
