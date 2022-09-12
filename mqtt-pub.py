import time
from random import uniform

import paho.mqtt.client as mqtt


def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("connected")
    else:
        print("problem , rc : " + str(rc))


def on_publish(client, userdata, mid):
    print("mid: " + str(mid))
    pass



mqttc = mqtt.Client("pub")
mqttc.on_connect = on_connect
mqttc.on_publish = on_publish

mqttc.username_pw_set("serge", "B1ua2gneOFnlhOOI")
mqttc.connect("serge.cloud.shiftr.io", 1883, 60)

while True:
    randNumber = uniform(19.0,21.0)
    mqttc.publish("temperature/room/1",randNumber)
    time.sleep(1)
