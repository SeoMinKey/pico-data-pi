from machine import Pin, PWM
import time
from notes import tones # /lib/notes.py 사용

# ---- 부저(PWM) 설정: GP22 ----
buzzer = PWM(Pin(22))

# ---- 간단한 재생 함수 ----
def play(note, beats, bpm=180, volume=30000):
    """
    note: "E7", "C7", "G6" 같은 음표 문자열, 휴식은 "R"
    beats: 음 길이 (박자 단위, 예: 1=4분음표, 0.5=8분음표)
    bpm: 분당 박자수(템포)
    volume: 소리 크기 (0~65535)
    """
    beat_sec = 60 / bpm          # 1박 길이(초)
    duration = beat_sec * beats  # 재생 시간(초)

    if note == "R":              # 휴식(쉼표)
        buzzer.duty_u16(0)
        time.sleep(duration)
        time.sleep(0.02)         # 짧은 간격
        return

    freq = tones.get(note)       # 음표 → 주파수(Hz)
    if freq is None:
        # 음표가 사전에 없으면 조용히 건너뜀
        buzzer.duty_u16(0)
        time.sleep(duration)
        time.sleep(0.02)
        return

    buzzer.freq(freq)
    buzzer.duty_u16(volume)
    time.sleep(duration)
    buzzer.duty_u16(0)
    time.sleep(0.02)             # 음과 음 사이의 짧은 간격

# ---- 슈퍼 마리오 메인 테마 (간단 발췌) ----
# 참고: 음 높이가 너무 높으면 부저/보드에 따라 작게 들리거나 안 들릴 수 있음
# 없는 음은 자동으로 건너뜁니다.
melody = [
    # 첫 구절
    ("E7", 0.5), ("E7", 0.5), ("R", 0.5), ("E7", 0.5),
    ("R", 0.5), ("C7", 0.5), ("E7", 0.5), ("R", 0.5),
    ("G7", 1.0), ("R", 1.0),

    # 둘째 구절
    ("G6", 0.5), ("R", 0.5), ("C7", 0.5), ("R", 0.5),
    ("G6", 0.5), ("R", 0.5), ("E6", 0.5), ("R", 0.5),

    # 셋째 구절(변주)
    ("A6", 0.5), ("R", 0.5), ("B6", 0.5), ("R", 0.5),
    ("AS6", 0.5), ("A6", 0.5), ("R", 0.5),
    ("G6", 0.5), ("E7", 0.5), ("G7", 0.5),
    ("A7", 0.5), ("R", 0.5), ("F7", 0.5), ("G7", 0.5),
    ("R", 0.5), ("E7", 0.5), ("C7", 0.5), ("D7", 0.5), ("B6", 1.0),
]

# ---- 재생 ----
# bpm(템포)와 volume(볼륨)을 필요에 따라 바꿀 수 있음
for note, beats in melody:
    play(note, beats, bpm=180, volume=28000)

# 끝난 후 완전히 끄기
buzzer.duty_u16(0)