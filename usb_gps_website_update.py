import requests
import io
import pynmea2
import serial
import json
import time

ser = serial.Serial('COM3', 9600)
sio = io.TextIOWrapper(io.BufferedRWPair(ser,ser))
buoy_id = 1



while True:
    strip = ser.readline() # read serial input
    if strip.find(b'GGA') > 0: # exclude all entries not starting with "GGA"
        msg = pynmea2.parse(strip.decode('utf-8')) # parse the incoming serial string to a "Location"-Object
        print(msg) # print data from "Location"-Object
        r = requests.post(
            'https://test.regattatracker.nl/api/buoys/' + str(buoy_id) + '/positions', 
            data = {
                'api_key': '661876ad034b008a1dee9eecf024c9db',            
                'latitude': round(msg.latitude, 6),
                'longitude': round(msg.longitude, 6)
            }
        )
        print(r.text)
        
        time.sleep(5)
        
        



