### Humidity checker - Andrew R Gross - 2019-11-28

### Libraries
import Adafruit_DHT
import datetime
from time import sleep
import RPi.GPIO as GPIO
import sys

### Parameters
sensor = Adafruit_DHT.DHT11
pin = 4
setpoint = 20

GPIO.setmode(GPIO.BCM)
GPIO.setup(17, GPIO.OUT)
logfile = open("/home/pi/diy/humidity-controller/humidity-temperature-log.csv", 'a')

if len(sys.argv) > 1:
	setpoint = float(sys.argv[1])
else:
	pass

print('Setpoint = ' + str(setpoint))

while True:

	time = datetime.datetime.now()
	humidity, temperature = Adafruit_DHT.read_retry(sensor,pin)
	print('Temp={0:0.1f}*  Humidity={1:0.1f}%'.format(temperature, humidity))
#	print(str(humidity))
#	print('humidity + 100')

	if humidity < setpoint:
		humiditystate = 'Humidity low'
		print('Humidity is low')
		GPIO.output(17, 1)
	else:
		humiditystate = 'Humidity nominal'
		GPIO.output(17, 0)

	new_line = time.strftime('%a %Y-%m-%d, %H:%M:%S, ') + str(temperature) + ' C, ' +  str(humidity) + '%, ' + humiditystate + '\n'
	print(new_line)

	logfile = open('/home/pi/diy/humidity-controller/humidity-temperature-log.csv', 'r') # Open log file in append mode
	contents = logfile.readlines()
	contents.insert(0, new_line)
	logfile.close()
	logfile = open('/home/pi/diy/humidity-controller/humidity-temperature-log.csv', 'w')
	logfile.writelines(contents)
	logfile.close()

	sleep(300)

