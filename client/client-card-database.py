import requests
import nfc
import time
from datetime import datetime, timezone
import pytz
import cv2
import subprocess

def main():
    subprocess.Popen(['mpg321', './sound/client-card-database-start.mp3'])
    japan_tz = pytz.timezone('Asia/Tokyo')

    camera = cv2.VideoCapture(0)
    camera.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
    camera.set(cv2.CAP_PROP_BUFFERSIZE, 1)
    clf = nfc.ContactlessFrontend('usb')
    try:
        while True:
            tag = clf.connect(rdwr={'on-connect': lambda tag: False})
            id = tag.identifier.hex().upper()
            jst_time = datetime.now(japan_tz).strftime('%Y-%m-%d %H:%M:%S')
            camera_file = datetime.now(japan_tz).strftime('%Y-%m-%d-%H-%M-%S') + '.jpg'
            
            print(jst_time, id)

            while True:
                for _ in range(5):
                    camera.grab()
                ret, frame = camera.read()
                if ret:
                    break
            retval, frame_encoded = cv2.imencode('.jpg', frame)
            cv2.waitKey(1)
            
            new_data = {'time': jst_time, 'card': id, 'camera': camera_file}
            try:
                response = requests.post('http://172.16.24.77:6500/insert_card_data', json=new_data)
                print(response.text)
                files = {'file': (camera_file, frame_encoded)}            
                response = requests.post('http://172.16.24.77:6500/upload-image', files=files)
                subprocess.run(['mpg321', './sound/card-info-transmitted.mp3'])
            except:
                subprocess.run(['mpg321', './sound/network-error.mp3'])
                print('Network Error!')
    finally:
        clf.close()

if __name__ == '__main__':
    main()
