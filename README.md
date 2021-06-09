# Smart Building Project - Cloud Platform

This repository contains the implementation of the Cloud backend.

## MQTT edge connection

Data cinoming form the edge architecture arrives through MQTT. A broker is started on the cloud.

## Services 

- Temperature
- Presence (QR)
- Humidity
- Automation (Through decision making)

## Telegram notification system

Telegram is used to send notifications to people in a room that has the possibility of having an higher rate of covid spread. User data is obtained through the QR system and is then saved on an in-memory data store.

## Decision making

The decision making algorithm is integrated as a git submodule, using a reference to the SB-DecisionMaking repository.

