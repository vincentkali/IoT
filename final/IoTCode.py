import base64
import sys
import signal

import requests
import http.client, urllib
import socket
import json


import time                
import RPi.GPIO as GPIO  
import os

from picamera import PiCamera



sys.path.append('/home/pi/rpi/code/Package')

### buzzer setting ###
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

BUZZER_PIN = 23
BUTTON_PIN = 24
GPIO.setup(BUZZER_PIN,GPIO.OUT)
GPIO.setup(BUTTON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
### buzzer setting ###

deviceId = "DCj00ERw"
deviceKey = "ESFBWzz2dhWom2kg"

def get_to_mcs():
    host = "http://api.mediatek.com"
    endpoint = "/mcs/v2/devices/" + deviceId + "/datachannels/buzzer/datapoints"
    url = host + endpoint
    headers = {"Content-type": "application/json", "deviceKey": deviceKey}
    r = requests.get(url,headers=headers)
    value = (r.json()["dataChannels"][0]["dataPoints"][0]["values"]["value"])
    return value

def post_to_mcs(payload):  
    headers = {"Content-type": "application/json", "deviceKey": deviceKey}
    not_connected = 1
    while (not_connected):
        try:
            conn = http.client.HTTPConnection("api.mediatek.com:80")
            conn.connect()
            print("connection succeed")
            not_connected = 0
        except (http.client.HTTPException) as ex:
            print("Error: %s" % ex)
            time.sleep(10)  # sleep 10 seconds

    conn.request("POST", "/mcs/v2/devices/" + deviceId + "/datapoints", json.dumps(payload), headers)
    response = conn.getresponse()
    print( response.status, response.reason, json.dumps(payload), time.strftime("%c"))
    data = response.read()
    conn.close()

def alert():
    camera()
    line_notify_image()
    #line_notify_msg()
    buzz()
    
def line_notify_image():
    os.system("""curl -H "Authorization: Bearer ebNm5twYljYeNQKqHOkBgnCDjIvMcLwDwzonqKMA9FL" 
    -X POST https:/notify-api.line.me/api/notify  -F "message=alert!!!" -F "imageFile=@image.jpg"
    """)

def line_notify_msg():
    os.system("""curl -H "Authorization: Bearer ebNm5twYljYeNQKqHOkBgnCDjIvMcLwDwzonqKMA9FL" 
    -X POST https:/notify-api.line.me/api/notify  -F "message=alert!!!"
    """)

def camera():
    camera = PiCamera()
    camera.rotation = 180
    camera.capture('/home/pi/Desktop/image.jpg')

def buzz():
    for i in range(200):
        GPIO.output(BUZZER_PIN,True)
        time.sleep(0.1)
        GPIO.output(BUZZER_PIN,False)
        time.sleep(0.1)
        if GPIO.input(BUTTON_PIN) == GPIO.LOW:
            payload = {"datapoints":[{"dataChnId":"buzzer","values":{"value":str(0)}}]}
            post_to_mcs(payload)
            break




def main():
    while(True):
        if (get_to_mcs() == "1"):
            alert()
        time.sleep(0.5)
        

try:
    print('按下 Ctrl-C 可停止程式')
    main()
except KeyboardInterrupt:
    print('關閉程式')
finally:
    GPIO.cleanup()

