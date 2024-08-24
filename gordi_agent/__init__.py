import os
import json
import paho.mqtt.client as mqtt

BROKER_IP = os.getenv("BROKER_IP")
BROKER_PORT = int(os.getenv("BROKER_PORT"))
BROKER_USER = os.getenv("BROKER_USER")
BROKER_PASS = os.getenv("BROKER_PASS")

LIGHT_TOPIC = "shellies/shellyswitch25-C45BBE7661F1/relay/0/command"
FAN_TOPIC = "shellies/shellyswitch25-C45BBE7661F1/relay/1/command"
BUTTON_TOPIC = "zigbee2mqtt/marc-magic-button"


def on_connect(client, userdata, flags, reason_code, properties):
    if reason_code == 0:
        print("Connected to MQTT broker successfully")
        client.subscribe(BUTTON_TOPIC)
    else:
        print(f"Failed to connect, return code {reason_code}\n")


def on_disconnect(client, userdata, reason_code):
    print(f"Disconnected from MQTT broker with return code {reason_code}\n")


def on_message(client, userdata, msg):
    # print(f"Message received on topic {msg.topic}: {msg.payload.decode()}")
    event = json.loads(msg.payload.decode().strip())
    action = event['action']

    if msg.topic == BUTTON_TOPIC:
        control_light(client, event)

    if msg.topic == FAN_TOPIC:
        control_fan(client, event)


def single(client):
    result = client.publish(LIGHT_TOPIC, "toggle")

    # Check if the publish was successful
    if result[0] == 0:
        print("Message sent: toggle")
    else:
        print(f"Failed to send message to topic {LIGHT_TOPIC}")


def hold(client):
    result = client.publish(FAN_TOPIC, "toggle")

    # Check if the publish was successful
    if result[0] == 0:
        print("Message sent: toggle")
    else:
        print(f"Failed to send message to topic {LIGHT_TOPIC}")


def control_light(client, event):
    match event["action"]:
        case "single":
            return single(client)
        case "hold":
            return hold(client)
        case _:
            return "Default case: Value not recognized"


def control_fan(client, payload):
    event = payload.decode().strip()
    print(f"event: {event}")


def main():
    mqttc = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)

    mqttc.on_connect = on_connect
    mqttc.on_disconnect = on_disconnect
    mqttc.on_message = on_message

    mqttc.username_pw_set(BROKER_USER, BROKER_PASS)
    mqttc.connect(BROKER_IP, BROKER_PORT, 60)

    # Start the loop to process network traffic and dispatch callbacks
    mqttc.loop_forever()

