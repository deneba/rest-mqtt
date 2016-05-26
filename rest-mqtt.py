# Title: Script to catch rest calls for home automation and forward to MQTT (rest-mqtt)
# Author: Dr. Asif Rana (aiqbalrana@gmail.com)
# Date: 20160525

from flask import Flask
from flask import request
from flask_restful import Resource, Api
import paho.mqtt.publish as publish
import paho.mqtt.client as mqtt
import time
import sys
import ConfigParser
import json

config = ConfigParser.ConfigParser()
config.read("code-list.txt")

# Topic on which the broker or other mqtt clients are listening
topic = "/home/command/switchthings"

app = Flask(__name__)
api = Api(app)

class EasyHomeSwitch(Resource):
    def post(self):
        try:
            rdata = request.data
            kdata = rdata.replace("\n","")
            kdata = json.dumps(kdata)
            kdata = json.loads(kdata)
            kdata = eval(str(kdata))
            # REST key value pair. The used key here is "skey"
            topicdata =  kdata["skey"].strip()
	    command = config.get('EasyHomeList', str(topicdata))
	    client = mqtt.Client()
      # Host address of mqtt (e.g., mosquitto broker)
	    client.connect("192.11.3.212")
      client.publish(topic, command)
	    client.disconnect()
	    print("Time:" + time.strftime("%d/%b/%y %H%M%S",time.localtime()) + ", Sent => Topic:" + topic + ", Data: " + command);
            return {'status': 'success'}
	except Exception,e:
            print("Error: " + str(e))

api.add_resource(EasyHomeSwitch, '/EasyHomeSwitch')

if __name__ == '__main__':
    # Bind to any ip on this host
    app.run(debug=False, host='0.0.0.0')
