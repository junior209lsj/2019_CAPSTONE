#import paho.mqtt.publish as publish
import paho.mqtt.client as mqtt
import serial
from PMS7003 import PMS7003

import sqlite3 as lite
import time

# broker setting
MQTT_SERVER = 'iot.eclipse.org'
MQTT_PORT = 1883

maqttC = mqtt.Client()
maqttC.connect(MQTT_SERVER, MQTT_PORT)


dust = PMS7003()

# Baud Rate
Speed = 9600

# UART / USB Serial
USB0 = '/dev/ttyUSB0'
UART = '/dev/ttyAMA0'

# USE PORT
SERIAL_PORT = USB0
 
#serial setting
ser = serial.Serial(SERIAL_PORT, Speed, timeout = 1)

#initallizing
buffer = ser.read(1024)

if(dust.protocol_chk(buffer)):
  data = dust.unpack_data(buffer)

  print ("PMS 7003 dust data")
  print ("PM 1.0 : %s" % (data[dust.DUST_PM1_0_ATM]))
  print ("PM 2.5 : %s" % (data[dust.DUST_PM2_5_ATM]))
  print ("PM 10.0 : %s" % (data[dust.DUST_PM10_0_ATM]))

else:
  print ("data read Err")

#DB connecting
database_filename = 'dustData.db'
conn = lite.connect(database_filename)
cs = conn.cursor()

#drop table
query = "DROP TABLE IF EXISTS t1"
cs.execute(query)

#create table
query = "CREATE TABLE IF NOT EXISTS t1 (data1, data2, data3, at DATETIME)"
cs.execute(query)


print("hhhh")

while True :
  
  #insert table
  time.sleep(1)
  PMdata = data[dust.DUST_PM1_0_ATM], data[dust.DUST_PM2_5_ATM], data[dust.DUST_PM10_0_ATM]
  
  #peak value elimination
  if data[dust.DUST_PM1_0_ATM] < 300 and data[dust.DUST_PM2_5_ATM] < 300 and data[dust.DUST_PM10_0_ATM] < 300:
    query = "INSERT into t1 values (?, ?, ?, DATETIME('NOW'))"
    cs.execute(query,(PMdata))
     
    #publishing data to client
    maqttC.publish(topic="PMdata", payload=data[dust.DUST_PM1_0_ATM] , qos=0, retain=False)

  conn.commit()
  
  
  
  #########
  print ("PMS 7003 dust data")
  print ("PM 1.0 : %s" % (data[dust.DUST_PM1_0_ATM]))
  print ("PM 2.5 : %s" % (data[dust.DUST_PM2_5_ATM]))
  print ("PM 10.0 : %s" % (data[dust.DUST_PM10_0_ATM]))
  #########
  
  #new data unpacking
  ser.flushInput()
  buffer = ser.read(1024)
  data = dust.unpack_data(buffer)



# closig
cs.close()
conn.close()
