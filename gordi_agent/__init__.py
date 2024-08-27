import os
import json
import asyncio
import aiomqtt
import time
import logging
from typing import Awaitable

from devices import Button

BROKER_IP = os.getenv("BROKER_IP")
BROKER_PORT = int(os.getenv("BROKER_PORT"))
BROKER_USER = os.getenv("BROKER_USER")
BROKER_PASS = os.getenv("BROKER_PASS")

LIGHT_TOPIC = "shellies/shellyswitch25-C45BBE7661F1/relay/0/command"
FAN_TOPIC = "shellies/shellyswitch25-C45BBE7661F1/relay/1/command"
BUTTON_TOPIC = "zigbee2mqtt/marc-magic-button"


async def single_press_action(client, event):
    print("Single press detected!")
    await client.publish(LIGHT_TOPIC, payload="toggle")


def fan_toggle(client) -> Awaitable[None]:
    logging.info("fan state toggled...")
    return client.publish(FAN_TOPIC, payload="toggle")


def fan_off(client) -> Awaitable[None]:
    logging.info("fan state off...")
    return client.publish(FAN_TOPIC, payload="off")


# QUESTION: Does this behaves as a singleton?
ongoing_delays = {}
async def hold_action(client, event):
    if client in ongoing_delays:
        ongoing_delays[client].cancel()
    
    await fan_toggle(client)

    async def delayed_stop():
        try:
            await asyncio.sleep(20)
            await fan_off(client)
        except asyncio.CancelledError:
            print("Delay cancelled")

    ongoing_delays[client] = asyncio.create_task(delayed_stop())


async def single_press_action2(client, event):
    print("foo bar")


async def hold_action2(client, event):
    print("baz")


async def listen(client: aiomqtt.Client, buttons):
    async for message in client.messages:
        event = json.loads(message.payload.decode().strip())
        await asyncio.gather(*(button.handle_event(client, event) for button in buttons))


async def main():
    logging.basicConfig(level=logging.DEBUG)
    client = aiomqtt.Client(
        hostname=BROKER_IP,
        port=BROKER_PORT,
        username=BROKER_USER,
        password=BROKER_PASS
    )

    # Connect to the MQTT broker and start subscribing to the topic
    async with client:
        # Initialize the Button instance with the callbacks
        button = Button(client, on_single=single_press_action, on_hold=hold_action)
        button2 = Button(client, on_single=single_press_action2)

        await client.subscribe(BUTTON_TOPIC)

        # Use a task group to manage and await all worker tasks
        async with asyncio.TaskGroup() as tg:
            tg.create_task(listen(client, [button, button2]))


asyncio.run(main())
