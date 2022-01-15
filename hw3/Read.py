import time
import RPi.GPIO as GPIO
from mfrc522 import MFRC522
import requests
import signal
import httplib, urllib  
import json  
import sys  
sys.path.append('/home/pi/rpi/code/Package')  

deviceId = "XXXXXXXX"  
deviceKey = "XXXXXXXXXXXXXX"

#**************************************************** 
# Set MediaTek Cloud Sandbox (MCS) Connection                                                   
#**************************************************** 

def post_to_mcs(payload):  
    headers = {"Content-type": "application/json", "deviceKey": deviceKey}
    not_connected = 1
    while (not_connected):
        try:
            conn = httplib.HTTPConnection("api.mediatek.com:80")
            conn.connect()
            print("connection succeed")
            not_connected = 0
        except (httplib.HTTPException) as ex:
            print "Error: %s" % ex
            time.sleep(10)  # sleep 10 seconds

    conn.request("POST", "/mcs/v2/devices/" + deviceId + "/datapoints", json.dumps(payload), headers)
    response = conn.getresponse()
    print( response.status, response.reason, json.dumps(payload), time.strftime("%c"))
    data = response.read()
    conn.close()

def get_to_mcs():
    host = "http://api.mediatek.com"
    endpoint = "/mcs/v2/devices/" + deviceId + "/datachannels/dis/datapoints"
    url = host + endpoint
    headers = {"Content-type": "application/json", "deviceKey": deviceKey}
    r = requests.get(url,headers=headers)
    value = (r.json()["dataChannels"][0]["dataPoints"][0]["values"]["value"])
    return value

GPIO.setmode(GPIO.BOARD)

LED0    = 7   
LED1    = 11
counter = 0

GPIO.setup(LED0,GPIO.OUT)
GPIO.setup(LED1,GPIO.OUT)

continue_reading = True

def end_read(signal,frame):
    global continue_reading
    continue_reading = False
    GPIO.cleanup()


signal.signal(signal.SIGINT, end_read)


MIFAREReader = MFRC522()



while continue_reading:   
    (status,TagType) = MIFAREReader.MFRC522_Request(MIFAREReader.PICC_REQIDL)
    if status == MIFAREReader.MI_OK:
        print ("Card detected")
    (status,uid) = MIFAREReader.MFRC522_Anticoll()
    if status == MIFAREReader.MI_OK:
        print ("Card read UID: "+str(uid[0])+","+str(uid[1])+","+str(uid[2])+","+str(uid[3]))
        #defaultS
        key = [0xFF,0xFF,0xFF,0xFF,0xFF,0xFF]
        MIFAREReader.MFRC522_SelectTag(uid)
        stored_uid = str(uid[0]) + str(uid[1]) + str(uid[2]) + str(uid[3])
        print (stored_uid)
        status = MIFAREReader.MFRC522_Auth(MIFAREReader.PICC_AUTHENT1A, 8, key, uid)
    
        payload = {"datapoints":[{"dataChnId":"id","values":{"value":stored_uid}}]}
        post_to_mcs(payload)
        
        if status == MIFAREReader.MI_OK:
	    payload = {"datapoints":[{"dataChnId":"led","values":{"value":str(1)}}]}
            post_to_mcs(payload)
            MIFAREReader.MFRC522_Read(8)
            MIFAREReader.MFRC522_StopCrypto1()
        else:
	    payload = {"datapoints":[{"dataChnId":"led","values":{"value":str(0)}}]}
            post_to_mcs(payload)
            print ("Authentication error")
	if get_to_mcs() == 1:
	    GPIO.output(LED0,GPIO.HIGH)
            time.sleep(0.5)
            GPIO.output(LED0,GPIO.LOW)
	else:
	    GPIO.output(LED1,GPIO.HIGH)
            time.sleep(0.5)
            GPIO.output(LED1,GPIO.LOW)


