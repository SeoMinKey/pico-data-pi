from machine import Pin
import neopixel  # 펌웨어에 내장되어 있어서 별도 설치 불필요
import time

PIXEL_PIN = 21
PIXEL_COUNT = 1

np = neopixel.NeoPixel(Pin(PIXEL_PIN), PIXEL_COUNT)

# 바꿔가며 사용할 색 목록
colors = [
    (255, 0, 0),  # 빨강
    (0, 255, 0),  # 초록
    (0, 0, 255),  # 파랑
    (255, 255, 0),  # 노랑
    (0, 255, 255),  # 시안
    (255, 0, 255),  # 자홍
    (255, 255, 255),  # 흰색
]

while True:
    for c in colors:
        np[0] = c
        np.write()
        time.sleep(0.5)  # 0.5초마다 색 변경
