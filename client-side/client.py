import os
import sys
import paho.mqtt.client as mqtt
import Adafruit_DHT
import time

#SERVER="172.20.83.31"
SERVER="localhost"
CLIENT_NAME="Stacja"
STATION_ID=1 # This station unique ID
JUST_DEBUG=False

sensors = [15, 4, 14, 26] # GPIOs (BCM notation) to which sensors are connected
temps = []
hums = []


client = mqtt.Client(CLIENT_NAME)
client.connect(SERVER)

def client_pub(topic, msg):
    global client
    global JUST_DEBUG
    if JUST_DEBUG:
        print("[%s] %s" % (topic, msg) )
    else:
        client.publish(topic, msg)

for i in range(0, 200):
    timestamp = int(time.time())
    d = 0
    temps = []
    hums = []
    for x,s in enumerate(sensors):
        humidity, temp = Adafruit_DHT.read_retry(11, s, delay_seconds=0.2)
        if humidity is not None:
            print '#{0:d}/{1:d} Temp {2:0.1f} C {3:0.1f} %'.format(s, timestamp, temp, humidity)
            temps.append(temp)
            hums.append(humidity)

    # Interpolate with some weights
    for i,t in enumerate(temps):
        d += 1
        if i > 0:
            for aaa in range(0, 100):
                weight_left = aaa * 1.0 / 100.0
                weight_right = 1.0 - weight_left
                tt = temps[i-1] * weight_left + t * weight_right
                hh = hums[i-1] * weight_left + hums[i] * weight_right
                client_pub("sensors/station{0:d}/sensor{1:d}/{2:d}/temp".format(STATION_ID, d, timestamp),"{0:0.1f}".format(tt))
                client_pub("sensors/station{0:d}/sensor{1:d}/{2:d}/hum".format(STATION_ID, d, timestamp),"{0:0.1f}".format(hh))
                d += 1
        client_pub("sensors/station{0:d}/sensor{1:d}/{2:d}/temp".format(STATION_ID, d, timestamp),"{0:0.1f}".format(t))
        client_pub("sensors/station{0:d}/sensor{1:d}/{2:d}/hum".format(STATION_ID, d, timestamp),"{0:0.1f}".format(hums[i]))
        
