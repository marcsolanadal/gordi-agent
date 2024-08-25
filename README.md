# Gordi Agent

> In honor of my defunct beloved chicken, you will be named **Gordi**.

## Motivation

This repository is a proof of concept to test how difficult it is to automate the more stable parts of my home - like the shutters or fans.
I also want to create a **Telegram bot** to control those automations.

All my devices use MQTT as the communication protocol.

We're going to use **Python** as the language of choice. Here multiple reasons:

  - Easy and extensible
  - Good integration with AI
  - libraries: 
    - [`paho-mqtt`](https://pypi.org/project/paho-mqtt/)
    - [`aiomqtt`](https://github.com/empicano/aiomqtt) -> paho-mqtt with asyncio
    - [`python-telegram-bot`](https://python-telegram-bot.org/)
    - [`pyephem`](https://rhodesmill.org/pyephem/rise-set.html) -> astronomic positions

One of the main motivators to use a programming language with only an MQTT client is to reduce complexity. 
Right now, I have all my automations in Node-RED. 
Although it is a great tool for hacking automations, I don't like the "no code" approach. 
I want to have absolute control over my automations, understand what they do at a basic level and have version control.

The idea is to have this program running as a system service in my Nixos home automation machine (*casa*).

## Questions

- What is *wheel* when running `poetry build`?
- In *NIX* what's the difference between `buildInputs` and `nativeBuildInputs`?
