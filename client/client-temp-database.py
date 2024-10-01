import requests
import time
from datetime import datetime, timezone
import pytz
import Adafruit_BMP.BMP085 as BMP085
import RPi.GPIO as GPIO
import threading

mode = 0

def blink_led():
    GPIO_LED_PIN = 0    
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(GPIO_LED_PIN, GPIO.OUT)

    while True:
        GPIO.output(GPIO_LED_PIN, GPIO.HIGH)
        time.sleep(0.1)
        GPIO.output(GPIO_LED_PIN, GPIO.LOW)
        time.sleep(0.1)
        if mode == 0:
            GPIO.output(GPIO_LED_PIN, GPIO.HIGH)        
            time.sleep(0.1)
            GPIO.output(GPIO_LED_PIN, GPIO.LOW)
            time.sleep(2.0)
        
def main():
    global mode
    blink_led_thread = threading.Thread(target=blink_led, daemon=True)
    blink_led_thread.start()
    
    japan_tz = pytz.timezone('Asia/Tokyo')
    sensor = BMP085.BMP085()
        
    while True:
        jst_time = datetime.now(japan_tz).strftime('%Y-%m-%d %H:%M:%S')
        room_temp = sensor.read_temperature()
        
        new_data = {'time': jst_time, 'temp': room_temp}
        try:
            response = requests.post('http://172.16.24.77:6500/insert_temp_data', json=new_data)
            print(response.text)
            mode = 0
        except:
            print('Server Error!!')
            mode = 1
        time.sleep(60)

if __name__ == '__main__':
    main()
