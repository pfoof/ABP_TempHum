## Structure of the *system*

### Overall

![Image of the structure](https://github.com/pfoof/ABP_TempHum/raw/master/abp_szklarnia.svg "System structure")

### Business processes

![Business processes](https://github.com/pfoof/ABP_TempHum/raw/master/mqtt_recv_message.svg "Business processes")


## Database record structure
```
mongo -> db: sensors
                |
            --------
           |        |
   temperatures    humidities
        |
   { station_id }
   { timestamp  }
   { sensor_id  }
   { value      }
     
```

## Setting up the server
1. Install MQTT broker such as mosquitto
```
yum install epel-release
yum install mosquitto
systemctl enable mosquitto
mkdir /var/lib/mosquitto/
chown mosquitto:mosquitto /var/lib/mosquitto/
```
2. Install MongoDB (can be with Docker)
```
docker pull mongo
docker run -d  -p 27017:27017 mongo
```
3. Get needed Python packages
```
yum install python-pip
pip install Flask
pip install pymongo
pip install paho-mqtt
```
## Running
Running can be done with some docker image of Python or directly.
```
python server.py &
FLASK_APP=report.py flask run &
```

## Client side

*TODO*

## Test board

![Test board pinout](https://github.com/pfoof/ABP_TempHum/raw/master/testboard.svg "Test board pinout")