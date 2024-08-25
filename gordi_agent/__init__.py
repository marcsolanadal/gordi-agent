import os
import json
import asyncio
import aiomqtt
import time

from devices import Button

BROKER_IP = os.getenv("BROKER_IP")
BROKER_PORT = int(os.getenv("BROKER_PORT"))
BROKER_USER = os.getenv("BROKER_USER")
BROKER_PASS = os.getenv("BROKER_PASS")

LIGHT_TOPIC = "shellies/shellyswitch25-C45BBE7661F1/relay/0/command"
FAN_TOPIC = "shellies/shellyswitch25-C45BBE7661F1/relay/1/command"
BUTTON_TOPIC = "zigbee2mqtt/marc-magic-button"


async def single_press_action(event):
    print("Single press detected!")

async def hold_action(event):
    print("Hold detected!")

async def single_press_action2(event):
    print("foo bar")

async def hold_action2(event):
    print("baz")

async def listen(client: aiomqtt.Client, buttons):
    async for message in client.messages:
        event = json.loads(message.payload.decode().strip())
        await asyncio.gather(*(button.handle_event(event) for button in buttons))

# TODO: Add observer pattern to subscribe N devices to M topics

async def main():
    # Initialize the aiomqtt client
    client = aiomqtt.Client(
        hostname=BROKER_IP,
        port=BROKER_PORT,
        username=BROKER_USER,
        password=BROKER_PASS
    )
    # Initialize the Button instance with the callbacks
    button = Button(on_single=single_press_action, on_hold=hold_action)
    button2 = Button(on_single=single_press_action2)

    # Connect to the MQTT broker and start subscribing to the topic
    async with client:
        await client.subscribe(BUTTON_TOPIC)

        # Use a task group to manage and await all worker tasks
        async with asyncio.TaskGroup() as tg:
            tg.create_task(listen(client, [button, button2]))


asyncio.run(main())
