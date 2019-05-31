import time
import re
import paho.mqtt.client as mqtt
from pymongo import MongoClient
import pprint
#pp = pprint.PrettyPrinter(indent=4)

SERVER_NAME="serwer"
HOST="localhost"

mongo = MongoClient('localhost', 27017)

client = mqtt.Client(SERVER_NAME)
client.connect(HOST)
client.loop_start()

db = mongo['sensors']

def on_message(client, userdata, message):
	print("Message ["+message.topic+"]: "+message.payload)
	r = re.match("^sensors/station([0-9]+)/sensor([0-9]+)/([0-9]+)/(temp|hum)$", message.topic)
	if r:
		msgdata = {
			'station': int(r.group(1)),
			'sensor': int(r.group(2)),
			'time': int(r.group(3)),
			'value': float(message.payload)
		}
		if r.group(4)=='temp':
			db.temperatures.insert_one(msgdata)
		elif r.group(4)=='hum':
			db.humidities.insert_one(msgdata)
		

client.on_message = on_message
client.subscribe("sensors/#")

try:
    while True:
        time.sleep(1)
 
except KeyboardInterrupt:
    print "exiting"
    client.disconnect()
    client.loop_stop()
