# Gordi Agent

> In honor of my defunct beloved chicken, you will be named **Gordi**.

## Motivation

This repository is a proof of concept to test how difficult it is to automate the more stable parts of my home - like the shutters or fans.
I also want to create a **Telegram bot** to control those automations.

All my devices use MQTT as the communication protocol. I have two options with the programming language:

1. *Python*
  - Easy and extensible
  - Good integration with AI
  - libraries: 
    - [`paho-mqtt`](https://pypi.org/project/paho-mqtt/)
    - [`python-telegram-bot`](https://python-telegram-bot.org/)
1. *Rust*
  - Might serve as an excuse to finally learn `rust`.
  - libraries:
    - [`paho-mqtt`](https://github.com/eclipse/paho.mqtt.rust)
    - [`teloxide`](https://github.com/teloxide/teloxide?tab=readme-ov-file)

One of the main motivators to use a programming language with only an MQTT client is to reduce complexity. 
Right now, I have all my automations in Node-RED. 
Although it is a great tool for hacking automations, I don't like the "no code" approach. 
I want to have absolute control over my automations, understand what they do at a basic level and have version control.

The idea is to have this program running as a system service in my Nixos home automation machine (*casa*).

