import json
import paho.mqtt.client as mqtt
import mysql.connector

BROKER = "localhost"
PORT = 1883

TOPICS = [
    ("ahuntsic/aec-iot/b3/team01/pi01/sensors/temperature", 0),
    ("ahuntsic/aec-iot/b3/team01/pi01/sensors/humidity", 0),
    ("ahuntsic/aec-iot/b3/team01/pi01/actuators/led/state", 1),
]

db = mysql.connector.connect(
    host="localhost",
    user="iot",
    password="iot123",
    database="smartlab",
)
cursor = db.cursor()

client = mqtt.Client(client_id="pi01-logger")


def on_connect(client, userdata, flags, rc, properties=None):
    if rc == 0:
        print("Logger connected")
        client.subscribe(TOPICS)
    else:
        print(f"Logger connect error rc={rc}")


def on_message(client, userdata, msg):
    payload = msg.payload.decode()

    try:
        data = json.loads(payload)
    except json.JSONDecodeError:
        print("Invalid JSON ignored:", payload)
        return

    topic = msg.topic
    device = data.get("device", "unknown")
    ts = data.get("ts")

    try:
        if "value" in data:
            query = """
                INSERT INTO telemetry(device, topic, value, unit, ts_utc)
                VALUES (%s, %s, %s, %s, %s)
            """
            cursor.execute(
                query,
                (
                    device,
                    topic,
                    data.get("value"),
                    data.get("unit"),
                    ts,
                ),
            )
        else:
            query = """
                INSERT INTO events(device, topic, payload, ts_utc)
                VALUES (%s, %s, %s, %s)
            """
            cursor.execute(query, (device, topic, payload, ts))

        db.commit()
        print("Saved:", topic)

    except mysql.connector.Error as e:
        print("DB error:", e)
        db.rollback()


client.on_connect = on_connect
client.on_message = on_message

client.connect(BROKER, PORT, keepalive=60)
client.loop_forever()
