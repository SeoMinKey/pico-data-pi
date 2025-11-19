from machine import Pin
import neopixel
import time
import urandom  # 랜덤 시간용

# ---- 핀/장치 설정 ----
PIXEL_PIN = 21      # 네오픽셀 데이터 핀 (GP21)
PIXEL_COUNT = 1     # LED 개수 (1개)
button = Pin(20, Pin.IN, Pin.PULL_UP)  # 버튼: 풀업 → 눌리면 0
np = neopixel.NeoPixel(Pin(PIXEL_PIN), PIXEL_COUNT)

def set_color(r, g, b):
    np[0] = (r, g, b)
    np.write()

def pressed():
    return button.value() == 0  # 눌리면 0

def main():
    print("반응속도 게임 시작! (버튼: GP20, 네오픽셀: GP21)")
    print("규칙: 빨강 → (랜덤 대기) → 초록. 초록이 되면 바로 버튼을 누르세요!")
    print("빨강일 때 누르면 False Start!")
    records = []  # 반응속도(ms) 기록 저장

    while True:
        # 준비: 빨강
        set_color(100, 0, 0)
        print("\n준비... (빨강)")

        # 랜덤 대기 (2000~4499 ms)
        wait_ms = 2000 + urandom.getrandbits(12) % 2500
        start_wait = time.ticks_ms()
        false_start = False

        # 대기 중 버튼 누르면 False Start
        while time.ticks_diff(time.ticks_ms(), start_wait) < wait_ms:
            if pressed():
                false_start = True
                break
            time.sleep_ms(5)

        if false_start:
            set_color(0, 0, 0)
            print("False Start! 너무 빨랐어요. 2초 후 재시작...")
            time.sleep(2)
            continue

        # GO: 초록, 타이머 시작
        set_color(0, 100, 0)
        print("GO! (초록) 지금 누르세요!")
        t_start = time.ticks_ms()

        # 버튼 눌릴 때까지 대기
        while not pressed():
            time.sleep_ms(1)

        # 반응속도 계산/출력
        rt = time.ticks_diff(time.ticks_ms(), t_start)  # ms
        records.append(rt)
        print("반응속도: {} ms".format(rt))

        # 라운드 종료 처리: LED 끄고 선택지 제공
        set_color(0, 0, 0)
        print("\n1) 다시하기   2) 종료")
        choice = input("선택: ").strip()

        if choice == "2":
            # 평균/최고 기록 출력 후 LED 끄고 종료
            if records:
                avg = sum(records) / len(records)
                best = min(records)
                print("\n--- 결과 ---")
                print("시도 횟수:", len(records))
                print("평균 반응속도: {:.1f} ms".format(avg))
                print("최고(가장 빠름): {} ms".format(best))
            else:
                print("\n기록이 없습니다.")
            set_color(0, 0, 0)  # 네오픽셀 끄기
            print("프로그램을 종료합니다.")
            return
        # choice가 그 외(빈 입력 포함)면 계속 반복

try:
    main()
except KeyboardInterrupt:
    # Ctrl-C 등 수동 종료 시 LED 끄고 마무리
    set_color(0, 0, 0)
    print("\n사용자 중단. LED를 끄고 종료합니다.")