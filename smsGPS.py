import serial
import os,time
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BOARD)
port=serial.Serial("/dev/ttyS0", baudrate=9600,timeout=3)

receiver = "+237*************" # put the number of receiver here
latitude = 4
longitude = 1
# Add into data base
from Mysql_Connection import MySqlConnection

connection = MySqlConnection("admin", "admin", "somnolence")

def gpsCoordinates():
    port.write(b' ATZ\r')
    time.sleep(1)
    port.write(b'AT+CMGF=1\r')
    time.sleep(1)
    port.write(b'AT+CGPSPWR=1\r')
    time.sleep(1)
    port.write(b'AT+CGNSSEQ=RMC\r')
    rcv=port.read(100)
    print(rcv)
    time.sleep(1)
    port.write(b'AT+CGNSINF\r')
    rcv=port.read(100)
    print(rcv)
    time.sleep(2)
    msg=rcv.decode("UTF-8")
    chunks = msg.split(',')
    print(chunks[3])

    return chunks[3],chunks[4],chunks[6]

def sendSms2():
    port.write(b' ATZ\r')
    time.sleep(1)
    port.write(b'AT+CMGF=1\r')
    time.sleep(0.5)
    port.write(b'AT+CMGS="'+receiver.encode()+b'"\r"')
    time.sleep(0.5)
    msg="http://maps.google.com/maps?q=loc:"
    port.write(msg.encode()+str(latitude).encode()+b","+str(longitude).encode()+b"\r")
    time.sleep(0.5)
    port.write(bytes([26]))
    time.sleep(1)
    print("message sent...")

def sendSms1():
    port.write(b' ATZ\r')
    time.sleep(1)
    port.write(b'AT+CMGF=1\r')
    time.sleep(0.5)
    port.write(b'AT+CMGS="'+receiver.encode()+b'"\r"')
    time.sleep(0.5)
    msg="Alert drowsiness Driver"
    port.write(msg.encode() +b"\r")
    time.sleep(0.5)
    port.write(bytes([26]))
    time.sleep(1)
    print("message sent...")
    time.sleep(5)
    
def gpsCoordSMS():
    latitude,longitude,speed=gpsCoordinates()
    print('latitude :')
    print(latitude)
    print('longitude :')
    print(longitude)
    print('speed')
    print(speed)
    #sendSpeed()
    connection.add_parameters('MatriculeCar', 'Drowsiness', speed, longitude, latitude, 1)
    sendSms2()
    time.sleep(2)

