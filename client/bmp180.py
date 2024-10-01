import Adafruit_BMP.BMP085 as BMP085

sensor = BMP085.BMP085()
print('Temp = {0:0.2f} *C'.format(sensor.read_temperature()))
print(sensor.read_temperature())
