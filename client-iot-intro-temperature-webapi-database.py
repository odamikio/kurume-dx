import requests
import statistics
import time
from datetime import datetime
from zoneinfo import ZoneInfo

def main():
    japan_tz = ZoneInfo("Asia/Tokyo") 
    start_time = datetime.now(japan_tz).strftime('%Y-%m-%d %H:%M:%S')
    saved_temp = []
    saved_humid = []
    while True:
        jst_time = datetime.now(japan_tz).strftime('%Y-%m-%d %H:%M:%S')
        url = "http://192.168.10.101:1880/api/v2/device/sensor/value"
        try:
            response = requests.get(url)
            data = response.json()
            for item in data:
                if item["deviceId"] == 6:
                    print(jst_time)
                    print(item["values"])
                    temp = item["values"][0]
                    humid = item["values"][1]
                    saved_temp.append(temp)
                    saved_humid.append(humid)
                    new_data = {'time': jst_time, 'temp': temp}
                    try:
                        response = requests.post('http://192.168.10.103:6500/insert_temp_data',json=new_data)
                        print(response.text)
                    except:
                        print('Database Error!!')
        except:
            print('Server Error!!')
                 
        time.sleep(10)

if __name__ == '__main__':
    main()
