import json
import sqlite3 as sql
import paho.mqtt.client as mqtt

db = "bdd/temperature.sql"

alerte_min = "ALERTE - temperature inferieur a 23"
alerte_max = "ALERTE - temperature superieur ou egale à 24"


def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("connected")
        mqttc.subscribe("temperature/room/#")
    else:
        print("problem , rc : " + str(rc))


def on_message(client, userdata, msg):
    obs = json.loads(msg.payload)
    print(obs)
    print(msg.topic)

    with sql.connect(db) as con:
        c = con.cursor()
        c.execute(
            "INSERT INTO releve VALUES (?,?,?)",
            (obs["date"], obs["temperature"],msg.topic[-1]))

        if obs["temperature"] >= 24.0:
            c.execute("INSERT INTO alerte VALUES (?,?,?)",
                      (msg.topic[-1], obs["date"], alerte_max))

        elif obs["temperature"] < 23.0:
            c.execute("INSERT INTO alerte VALUES (?,?,?)",
                      (msg.topic[-1], obs["date"], alerte_min))


mqttc = mqtt.Client("sub")
mqttc.on_connect = on_connect
mqttc.on_message = on_message

# mqttc.username_pw_set("stitchtrack172", "hLlY9MPNPRw5ZCcX")
mqttc.connect("localhost", 1883)

mqttc.loop_forever()
