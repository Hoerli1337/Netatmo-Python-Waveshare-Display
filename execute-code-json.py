#!/usr/bin/python3 encoding=utf-8

import time
import os
from os.path import expanduser, exists
import lnetatmo
import json

config_file = open(expanduser("~/.netatmo.credentials"), "r")
lnetatmo_config = json.loads(config_file.read())

try:
	station_name = lnetatmo_config['STATION']
except:
	station_name = ""

authorization = lnetatmo.ClientAuth()
weather = lnetatmo.WeatherStationData(authorization)

user = weather.user

json_output = {}
#json_output[] = user.unit()

print("Station owner : ", user.mail)
# Das haut die MAC raus - print("Station name : ", station_name)

countloop = 1
for module, moduleData in weather.lastData(station=station_name, exclude=3600).items() :

        # Name of the module (or station embedded module)
        # You setup this name in the web netatmo account station management
        json_output[countloop] = {}
        json_output[countloop]['stationname'] = module
        json_output[countloop]['mainstation'] = weather.stations[station_name]['station_name']

        # List key/values pair of sensor information (eg Humidity, Temperature, etc...)
        for sensor, value in moduleData.items() :
            # To ease reading, print measurement event in readable text (hh:mm:ss)
            if sensor == "When" : value = time.strftime("%H:%M:%S",time.localtime(value))
            print("%30s : %s" % (sensor, value))
            json_output[countloop][sensor] = value
        
        countloop = countloop + 1

jsondata_output = json.dumps(json_output)

jsonfile = open("/home/pi/netatmo-api-python/weather.json", "w")
jsonfile.write(jsondata_output)
jsonfile.close()
