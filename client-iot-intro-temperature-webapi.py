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
                    saved_temp.append(item["values"][0])
                    saved_humid.append(item["values"][1])
        except:
            print('Server Error!!')

        mean_val = statistics.mean(saved_temp)
        median_val = statistics.median(saved_temp)
        max_val = max(saved_temp)
        min_val = min(saved_temp)

        print(f"==== from {start_time} to {jst_time}, data# is {len(saved_temp)} ====")
        print(f"mean: {mean_val:.2f}")
        print(f"median: {median_val:.2f}")
        print(f"max: {max_val:.2f}")
        print(f"min: {min_val:.2f}") 
        if len(saved_temp) >= 2:
            stdev_val = statistics.stdev(saved_temp)
            print(f"std deviation: {stdev_val:.2f}")   
        print("====================")                   
        time.sleep(10)

if __name__ == '__main__':
    main()
