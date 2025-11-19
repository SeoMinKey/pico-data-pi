"""
실습 파일 제목을 neopixel.py로 할 경우 에러가 나요
"""

from machine import Pin
import neopixel  # 펌웨어에 내장되어 있어서 별도 설치 불필요

# 네오픽셀 설정
PIXEL_PIN = 21  # 데이터 핀 (GP21)
PIXEL_COUNT = 1  # LED 개수 (여기서는 1개)

np = neopixel.NeoPixel(Pin(PIXEL_PIN), PIXEL_COUNT)

# 네오픽셀 켜기
np[0] = (255, 0, 0)  # (빨강, 초록, 파랑)
np.write()  # 적용
