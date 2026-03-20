import json
import time
from datetime import datetime, timezone

import board
import adafruit_dht
import paho.mqtt.client as mqtt

BROKER = "localhost"
PORT = 1883

DEVICE = "pi01"

TOPIC_TEMP_JSON = "ahuntsic/aec-iot/b3/team01/pi01/sensors/temperature"
TOPIC_TEMP_VALUE = "ahuntsic/aec-iot/b3/team01/pi01/sensors/temperature/value"
TOPIC_HUM_JSON = "ahuntsic/aec-iot/b3/team01/pi01/sensors/humidity"
TOPIC_HUM_VALUE = "ahuntsic/aec-iot/b3/team01/pi01/sensors/humidity/value"
TOPIC_STATUS = "ahuntsic/aec-iot/b3/team01/pi01/status/online"

# Sur Raspberry Pi/Linux, use_pulseio=False est souvent plus stable
dht = adafruit_dht.DHT22(board.D4, use_pulseio=False)

client = mqtt.Client(client_id="pi01-publisher")
client.will_set(TOPIC_STATUS, "offline", qos=1, retain=True)


def iso_utc_now():
    return datetime.now(timezone.utc).isoformat()


def on_connect(client, userdata, flags, rc, properties=None):
    if rc == 0:
        print("Connected to broker")
        client.publish(TOPIC_STATUS, "online", qos=1, retain=True)
    else:
        print(f"MQTT connect error rc={rc}")


client.on_connect = on_connect
client.connect(BROKER, PORT, keepalive=60)
client.loop_start()

try:
    while True:
        try:
            temperature = dht.temperature
            humidity = dht.humidity

            # sécurité minimale
            if temperature is None or humidity is None:
                print("Lecture invalide: valeur None")
                time.sleep(5)
                continue

            ts = iso_utc_now()

            payload_temp = {
                "device": DEVICE,
                "sensor": "temperature",
                "value": round(float(temperature), 2),
                "unit": "C",
                "ts": ts,
            }

            payload_hum = {
                "device": DEVICE,
                "sensor": "humidity",
                "value": round(float(humidity), 2),
                "unit": "%",
                "ts": ts,
            }

            client.publish(TOPIC_TEMP_JSON, json.dumps(payload_temp), qos=0)
            client.publish(TOPIC_TEMP_VALUE, str(payload_temp["value"]), qos=0)

            client.publish(TOPIC_HUM_JSON, json.dumps(payload_hum), qos=0)
            client.publish(TOPIC_HUM_VALUE, str(payload_hum["value"]), qos=0)

            print("TEMP:", payload_temp)
            print("HUM :", payload_hum)

        except RuntimeError as e:
            # normal avec DHT22: on log et on continue
            print("Erreur lecture capteur:", e)

        time.sleep(5)

except KeyboardInterrupt:
    print("Arrêt du publisher")

finally:
    try:
        dht.exit()
    except Exception:
        pass
    client.loop_stop()
    client.disconnect()
