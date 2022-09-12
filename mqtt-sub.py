import paho.mqtt.client as mqtt


def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("connected")
        mqttc.subscribe("temperature/room/#")
    else:
        print("problem , rc : " + str(rc))


def on_message(client, userdata, msg):
    print(str(msg.payload.decode()))


mqttc = mqtt.Client("sub")
mqttc.on_connect = on_connect
mqttc.on_message = on_message

mqttc.username_pw_set("stitchtrack172", "hLlY9MPNPRw5ZCcX")
mqttc.connect("stitchtrack172.cloud.shiftr.io", 1883)

mqttc.loop_forever()
