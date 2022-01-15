import time
import RPi.GPIO as GPIO
from mfrc522 import MFRC522
import signal

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
        status = MIFAREReader.MFRC522_Auth(MIFAREReader.PICC_AUTHENT1A, 8, key, uid)
    
        if status == MIFAREReader.MI_OK:
            MIFAREReader.MFRC522_Read(8)
            MIFAREReader.MFRC522_StopCrypto1()
            GPIO.output(LED0,GPIO.HIGH)
            time.sleep(0.5)
            GPIO.output(LED0,GPIO.LOW)
        else:
            print ("Authentication error")
            GPIO.output(LED1,GPIO.HIGH)
            time.sleep(0.5)
            GPIO.output(LED1,GPIO.LOW)
