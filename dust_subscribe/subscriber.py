import paho.mqtt.client as mqtt
import socket

import sqlite3 as lite
import time
import os
import subprocess

# command : ip route
MQTT_SERVER = 'iot.eclipse.org'
MQTT_PORT = 1883

#DB connecting
database_filename = 'dustData.db'
conn = lite.connect(database_filename)
cs = conn.cursor()

#drop table
query = "DROP TABLE IF EXISTS t1"
cs.execute(query)

#create table
os.system('/opt/ros/kinetic/setup.bash')
query = "CREATE TABLE IF NOT EXISTS t1 (data1, x, y, at DATETIME)"
cs.execute(query)


#####################################################
# on_connect() means that if we lose the connection and reconnect then subscriptions will be renewed.
# The callback for when the client receives a connect response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    #"PMdata" is just topic name
    client.subscribe('PMdata', qos=0)


def on_disconnect(client, userdata, rc):
    print("Client Got Disconnected")
    

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    os.system('/opt/ros/kinetic/setup.bash')
    print(msg.topic+" "+str(msg.payload))
    loc = os.popen('rostopic echo /odom -n1 | sed -n \'11,12p\'').read()
    loc = loc.split('\n', 2)
    x = float(loc[0].split(':', 2)[1])
    y = float(loc[1].split(':', 2)[1])
    
    msg.payload = str(msg.payload,"utf-8")

    #insert table
    query = "INSERT into t1 values (?, ?, ?, DATETIME('NOW'))"
    cs.execute(query, [msg.payload, x, y])
    
    # more callbacks, etc
    time.sleep(4)
 
    conn.commit()
    

########################################################3



client = mqtt.Client()

client.on_connect = on_connect
client.on_message = on_message

client.connect(MQTT_SERVER, MQTT_PORT)

client.loop_forever()


#conn.commit()
######################################################

# closig
cs.close()
conn.close()

# Blocking call that processes network traffic, dispatches callbacks and
# handles reconnecting.
# Other loop*() functions are available that give a threaded interface and a
# manual interface.






