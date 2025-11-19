from machine import Pin, I2C
import time
import network
import urequests
from ahtx0 import AHT20   # AHT20 sensor driver

# --------------------------
# WiFi 정보
# --------------------------
WIFI_SSID = "#############"    # 2.4G 네트워크 이름을 넣으세요 (5G 미지원)
WIFI_PASS = "#############"    # 네트워크 비밀번호

# --------------------------
# Google Apps Script Webhook URL
# --------------------------
WEBHOOK_URL = "##############"  # 구글 웹훅 URL

# --------------------------
# WiFi 연결 함수
# --------------------------
def connect_wifi():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    if not wlan.isconnected():
        print("WiFi 연결중...")
        wlan.connect(WIFI_SSID, WIFI_PASS)

        timeout = 0
        while not wlan.isconnected():
            time.sleep(0.2)
            timeout += 1
            if timeout > 60:  # 약 12초 후 포기
                print("WiFi 연결 실패. 재부팅 필요.")
                return False

    print("WiFi 연결됨:", wlan.ifconfig())
    return True

connect_wifi()

# --------------------------
# 센서 설정 (AHT20)
# --------------------------
i2c = I2C(0, sda=Pin(4), scl=Pin(5), freq=400000)

try:
    sensor = AHT20(i2c)
except Exception as e:
    print("AHT20 초기화 실패:", e)
    raise SystemExit

# --------------------------
# Google Sheet로 데이터 전송
# --------------------------
def send_to_google(temp, hum):
    data = {
        "temperature": round(temp, 2),
        "humidity": round(hum, 2),
        "device": "PicoW_AHT20"
    }

    try:
        res = urequests.post(
            WEBHOOK_URL,
            json=data,
            headers={"Content-Type": "application/json"}
        )

        # Google sometimes returns HTML even when successful.
        # Treat ANY 200-range status as success.
        if 200 <= res.status_code < 300:
            print("전송 성공")
        else:
            print("전송 실패 코드:", res.status_code)

        # Avoid printing HTML body
        res.close()

    except Exception as e:
        print("전송 오류:", e)

# --------------------------
# 메인 루프
# --------------------------
while True:
    t = sensor.temperature
    h = sensor.relative_humidity

    print("온도: {:.2f} °C  습도: {:.2f} %".format(t, h))

    send_to_google(t, h)

    time.sleep(5)   # 5초마다 업로드
