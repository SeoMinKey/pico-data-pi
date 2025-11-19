# --- 설정값 입력 ---
WIFI_SSID = "YOUR-WIFI-NAME"  # 2.4GHz 네트워크만 지원
WIFI_PASSWORD = "YOUR-PASSWORD-HERE"
OPENAI_API_KEY = "YOUR OPEN AI API KEY HERE"

# --- 기본 임포트 ---
from machine import Pin, PWM
import network
import time
import urequests  # /lib/urequests.py 필요
import ujson

# --- 핀 설정 ---
button = Pin(20, Pin.IN, Pin.PULL_UP)  # 버튼 (GP20, 풀업 사용 → 눌리면 0)
led = Pin("LED", Pin.OUT)  # 온보드 LED
buzzer = PWM(Pin(22))  # 부저(PWM) GP22 사용 (원하면 핀 변경)


# --- 부저 비프 함수 (아주 간단) ---
def beep(freq=1000, ms=120, pause_ms=80):
    buzzer.freq(freq)
    buzzer.duty_u16(30000)  # 볼륨 (0~65535)
    time.sleep_ms(ms)
    buzzer.duty_u16(0)
    time.sleep_ms(pause_ms)


# --- Wi-Fi 연결 ---
def wifi_connect():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    if not wlan.isconnected():
        wlan.connect(WIFI_SSID, WIFI_PASSWORD)
        for _ in range(40):  # 최대 약 8초 대기
            if wlan.isconnected():
                break
            time.sleep(0.2)
    return wlan.isconnected()


# --- ChatGPT에게 한국어 농담 요청 ---
def get_korean_joke():
    url = "https://api.openai.com/v1/chat/completions"
    headers = {
        "Content-Type": "application/json; charset=utf-8",
        "Authorization": "Bearer " + OPENAI_API_KEY,
    }
    payload_obj = {
        "model": "gpt-4o-mini",
        "messages": [
            {
                "role": "system",
                "content": "너는 짧고 재밌는 한국어 농담을 만드는 비서야.",
            },
            {"role": "user", "content": "웃긴 아재개그 알려줘"},
        ],
        "max_tokens": 200,  # 토큰한도
        "temperature": 0.1,  # 창의성
    }
    try:
        payload = ujson.dumps(payload_obj).encode("utf-8")  # bytes로 전송
        r = urequests.post(url, headers=headers, data=payload)
        if r.status_code != 200:
            txt = r.text
            r.close()
            return "HTTP 오류 {}: {}".format(r.status_code, txt)
        res = r.json()
        r.close()
        return res["choices"][0]["message"]["content"].strip()
    except Exception as e:
        return "요청 실패: {}".format(e)


# --- 메인 ---
def main():
    print("📡  Wi-Fi 연결 중...")
    if not wifi_connect():
        print("❌  Wi-Fi 연결 실패! SSID/비밀번호 확인하세요.\n\n")
        return

    # 연결 성공 신호: 부저 두 번 삐
    beep(1200, 120, 80)
    beep(1500, 120, 0)

    print("✅  Wi-Fi 연결 완료!")
    print("버튼(GP20)을 누르면 농담이 출력됩니다.\n\n")

    led.value(1)  # 동작 중 LED 켜기

    last = 0
    try:
        while True:
            # PULL_UP → 눌리면 0
            if button.value() == 0 and (time.ticks_ms() - last) > 300:
                last = time.ticks_ms()
                print("👉 ChatGPT에게 농담 요청...")
                joke = get_korean_joke()
                print("🤣 농담: \n", joke)
            time.sleep(0.02)
    except KeyboardInterrupt:
        # Ctrl-C 등으로 종료 시 여기로 옴
        pass
    finally:
        # 정리: LED 끄기, 부저 끄고 해제
        led.value(0)
        buzzer.duty_u16(0)
        try:
            buzzer.deinit()
        except:
            pass


# --- 실행 ---
main()
