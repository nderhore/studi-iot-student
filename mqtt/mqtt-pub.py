import json
import time
from random import uniform
from datetime import datetime
import threading

import paho.mqtt.client as mqtt

seuil_max = 25.0
seuil_min = 22.0


def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("connected")
    else:
        print("problem , rc : " + str(rc))


def thread_pub(mqttc, numero_salle):
    while True:
        data = {"date": datetime.now().isoformat(),
                "temperature": uniform(seuil_min, seuil_max)}
        mqttc.publish("temperature/room/" + str(numero_salle), json.dumps(data))
        time.sleep(1)


mqttc = mqtt.Client("pub")
mqttc.on_connect = on_connect
mqttc.connect("localhost", 1883, 60)

room1 = threading.Thread(target=thread_pub, args=(mqttc, 1))
room2 = threading.Thread(target=thread_pub, args=(mqttc, 2))
room3 = threading.Thread(target=thread_pub, args=(mqttc, 3))
room4 = threading.Thread(target=thread_pub, args=(mqttc, 4))

room1.start()
room2.start()
room3.start()
room4.start()
