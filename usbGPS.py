#!/usr/bin/env python
# encoding: utf-8

import json
import serial
import pynmea2
import calendar
from datetime import datetime
from tendo import singleton

me = singleton.SingleInstance() # will sys.exit(-1) if another instance of this script is already running


def mkEpoch(inputDatestamp, inputTimestamp):
	inputStr = inputDatestamp + " " + inputTimestamp

	datetimeObj = datetime.strptime(inputStr, "%Y-%m-%d %H:%M:%S")
	epochVal = calendar.timegm(datetimeObj.timetuple())

	return epochVal


def readSerial():
    serObj = serial.Serial("/dev/ttyACM0", 4800)
    streamReader = pynmea2.NMEAStreamReader()

    dateStamp = None
    signalStatus = None
    
    while True:
        dataObj = serObj.readline()
        for msgObj in streamReader.next(dataObj):
            outputObj = {}
            #print msgObj
            sentenceObj = pynmea2.parse(str(msgObj))
            if str(msgObj).startswith("$GPRMC"):
                dateStamp = msgObj.datestamp
                signalStatus = msgObj.status
            if str(msgObj).startswith("$GPGGA"):
                outputObj["latitude"] = msgObj.latitude
                outputObj["longitude"] = msgObj.longitude
                outputObj["gps_qual"] = msgObj.gps_qual
                outputObj["altitude"] = msgObj.altitude
                outputObj["altitude_units"] = msgObj.altitude_units
                outputObj["num_sats"] = msgObj.num_sats
                outputObj["horizontal_dil"] = msgObj.horizontal_dil
                outputObj["geo_sep"] = msgObj.geo_sep
                outputObj["geo_sep_units"] = msgObj.geo_sep_units
                outputObj["num_sats"] = msgObj.num_sats
                outputObj["timestamp"] = str(msgObj.timestamp)
                outputObj["age_gps_data"] = msgObj.age_gps_data
                outputObj["ref_station_id"] = msgObj.ref_station_id
                outputObj["dateStamp"] = str(dateStamp)
                outputObj["signalStatus"] = signalStatus
                outputObj["rxEpoch"] = mkEpoch(str(dateStamp), str(msgObj.timestamp))

                dataDir = "/home/pi/raspberry_ADS-B"
                filePath = dataDir + "/" + "currentLocation.json"
                open(filePath, "wb").write(json.dumps(outputObj))

                print outputObj

    return


def main():
    #print getLocation()
    try:
        readSerial()
    except KeyboardInterrupt:
        quit()

    except Exception,e:
        print e
        pass


if __name__ == "__main__":
    main()
