import pymongo

from flask import Flask
app = Flask(__name__)

mongo = pymongo.MongoClient()
db = mongo['sensors']

@app.route("/")
def index():
    return "Temperatures %d<br>Humidities %d" % (db.temperatures.count(), db.humidities.count())
