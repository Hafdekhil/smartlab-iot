import json
from datetime import datetime, timezone

import paho.mqtt.client as mqtt
from gpiozero import LED

BROKER = "localhost"
PORT = 1883

DEVICE = "pi01"

TOPIC_CMD = "ahuntsic/aec-iot/b3/team01/pi01/actuators/led/cmd"
TOPIC_STATE = "ahuntsic/aec-iot/b3/team01/pi01/actuators/led/state"

led = LED(17)
client = mqtt.Client(client_id="pi01-led")


def iso_utc_now():
    return datetime.now(timezone.utc).isoformat()


def publish_state(state):
    payload = {
        "device": DEVICE,
        "actuator": "led",
        "state": state,
        "ts": iso_utc_now(),
    }
    client.publish(TOPIC_STATE, json.dumps(payload), qos=1, retain=True)
    print("State published:", payload)


def on_connect(client, userdata, flags, rc, properties=None):
    if rc == 0:
        print("Connected")
        client.subscribe(TOPIC_CMD, qos=1)
        # publier l'état réel au démarrage
        publish_state("on" if led.is_lit else "off")
    else:
        print(f"MQTT connect error rc={rc}")


def on_message(client, userdata, msg):
    command = msg.payload.decode().strip().lower()
    print("Command:", command)

    if command == "on":
        led.on()
        publish_state("on")
    elif command == "off":
        led.off()
        publish_state("off")
    else:
        print("Invalid command ignored:", command)


client.on_connect = on_connect
client.on_message = on_message

client.connect(BROKER, PORT, keepalive=60)
client.loop_forever()
