import requests
import io
import pynmea2
import serial
import json
import time

ser = serial.Serial('COM3', 9600) # the serial port of the device -> change to /dev/ttyACM0 when using on pi
sio = io.TextIOWrapper(io.BufferedRWPair(ser,ser)) # serial reader buffer object
buoy_id = 1


while True:
    strip = ser.readline() # read serial input
    if strip.find(b'GGA') > 0: # exclude all entries not starting with "GGA"
        msg = pynmea2.parse(strip.decode('utf-8')) # parse the incoming serial string to a "Location"-Object
        print(msg) # print data from "Location"-Object
        try: # added try catch construction to catch a bug regarding checksum
            r = requests.post( # construct the post request
                'https://test.regattatracker.nl/api/buoys/' + str(buoy_id) + '/positions', 
                data = {
                    'api_key': '661876ad034b008a1dee9eecf024c9db',            
                    'latitude': round(msg.latitude, 6),
                    'longitude': round(msg.longitude, 6)
                }
            )
        except Exception: # catch any exception regarding the post request
            pass

        print(r.text)
        
        time.sleep(5) # limit the amount of updates, can be inproved with a duty cycle-like contruction