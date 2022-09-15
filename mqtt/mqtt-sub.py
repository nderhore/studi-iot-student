import datetime
import json
import pickle
import sqlite3 as sql
import paho.mqtt.client as mqtt
from googleapiclient.discovery import build
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
import os.path

# table sql
db = "./bdd/temperature.sql"
CREDENTIALS_FILE = './auth/credentials.json'

# token accès calendar
# alerte , regle de gestion
alerte_min = "ALERTE - temperature inferieur a 23"
alerte_max = "ALERTE - temperature superieur ou egale à 24"

SCOPES = ['https://www.googleapis.com/auth/calendar']


def createTokenAcess():
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('./auth/token.pickle'):
        with open('./auth/token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                CREDENTIALS_FILE, SCOPES)
            creds = flow.run_local_server(port=0)

        # Save the credentials for the next run
        with open('./auth/token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('calendar', 'v3', credentials=creds)
    return service


# recuperation des evenements googleCalendar
def get_event_calendrier(service):
    now = datetime.datetime.utcnow()
    now_s = now.isoformat() + 'Z'
    tomorrow = now + datetime.timedelta(days=1)
    tomorrow_s = tomorrow.isoformat() + 'Z'

    events_result = service.events().list(calendarId='primary', timeMin=now_s, timeMax=tomorrow_s,
                                          singleEvents=True, orderBy='startTime').execute()
    events = events_result.get('items', [])

    return events


# evenement recu lors de la connexion de notre script
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("connected")
        mqttc.subscribe("temperature/room/#")
    else:
        print("problem , rc : " + str(rc))

# evenement lors de la reception d'un message
def on_message(client, userdata, msg):
    obs = json.loads(msg.payload)
    print(obs)
    print(msg.topic)
    service = createTokenAcess()
    events = get_event_calendrier(service)

    with sql.connect(db) as con:
        c = con.cursor()
        c.execute(
            "INSERT INTO releve VALUES (?,?,?)",
            (obs["date"], obs["temperature"], msg.topic[-1]))

        if obs["temperature"] >= 24.0:
            c.execute("INSERT INTO alerte VALUES (?,?,?)",
                      (msg.topic[-1], obs["date"], alerte_max))

        elif obs["temperature"] < 23.0:
            c.execute("INSERT INTO alerte VALUES (?,?,?)",
                      (msg.topic[-1], obs["date"], alerte_min))

        for event in events:
            if str(msg.topic[-1]) == event['summary']:
                nombre_room = msg.topic[-1]
                temperature = c.execute(
                    "SELECT temperature from releve WHERE room = ? ORDER BY instant desc LIMIT 1",
                    nombre_room).fetchall()
                print(event)
                if temperature[0][0] < alerte_min:
                    print("RULES 3 : la temperature est inferieur au seuil et la salle est planifiée.")
                    c.execute("INSERT INTO alerte VALUES (?,?,?)",
                              (msg.topic[-1], obs["date"],
                               "RULES 3 : la temperature est inferieur au seuil et la salle est planifiée."))
                    break

                if temperature[0][0] > alerte_max:
                    print("RULES 3 : la temperature est superieur au seuil et la salle est planifiée.")
                    c.execute("INSERT INTO alerte VALUES (?,?,?)",
                              (msg.topic[-1], obs["date"],
                               "RULES 3 : la temperature est superieur au seuil et la salle est planifiée."))
                    break


mqttc = mqtt.Client("sub")
mqttc.on_connect = on_connect
mqttc.on_message = on_message

# mqttc.username_pw_set("stitchtrack172", "hLlY9MPNPRw5ZCcX")
mqttc.connect("localhost", 1883)

mqttc.loop_forever()
