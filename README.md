# Smart Building Project - Cloud Platform

This repository contains the implementation of the Cloud backend.

## Table of Contents

- [Smart Building Project - Cloud Platform](#smart-building-project---cloud-platform)
  - [Table of Contents](#table-of-contents)
  - [Introduction](#introduction)
  - [Application Setup](#application-setup)
    - [Local deploy with docker-compose](#local-deploy-with-docker-compose)
    - [Complete remote deploy with docker swarm](#complete-remote-deploy-with-docker-swarm)
  - [Edge and end device connection](#edge-and-end-device-connection)
    - [Edge devices MQTT connection](#edge-devices-mqtt-connection)
    - [QR interface](#qr-interface)
  - [Room APIs](#room-apis)
  - [Telegram notification system](#telegram-notification-system)
  - [Possible improvements](#possible-improvements)

## Introduction

The cloud backend is designed and implemented as a containerized application where each component is a microservice that focuses on a specific task, while exposing a set of HTTP APIs to provide a means of communication and interfacing.

The repository contains two files that can be used to locally setup a demo of the application, through a docker-compose stack, or to deploy a production-ready system through a swarm stack. 

## Application Setup

The application was developed as a series of containerized apps connected through HTTP APIs within Docker engine.

You can either set it up with a docker-compose stack, which is the setup used to develop the backend and to test it locally, or through a swarm stack, which reflects the production state, has an orchestrator and service replication but is longer and more complex as a process.

The cloud backend was developed and tested on a Ubuntu 21.04 machine with:
- Docker engine version 20.10.7
- docker-compose version 1.29.2

To install docker, refer to the [instructions on their website](https://docs.docker.com/engine/), depending on your platform.

### Local deploy with docker-compose

You need to have Docker engine, python3 and docker-compose installed on your machine to setup the compose stack. Python3 is generally included with every recent linux distribution, once you have it, you can install docker-compose through python package manager, pip:

```bash
pip3 install docker-compose
```

After it's installed, just clone this repository, change directory to the root of the cloud project and run:

```bash
docker-compose up --build -d
```

If you also want to use the telegram layer, you should create a new bot through the [official telegram botfather bot](https://telegram.dog/BotFather) and pass the bot secret token to the stack like this:

```bash
# for linux and unix-like
TELEGRAM_KEY="your bot token here" docker-compose up --build -d
```

### Complete remote deploy with docker swarm

You can deploy the swarm stack in two ways: either by using three different physical machines on the same subnet, or by using virtual machines.

You can also automate the VMs creation by using [docker-machine](https://docs.docker.com/machine/install-machine/). This last method is what it's used in this project, to deploy on the DigitalOcean platform.

Whatever method you choose, once you're ready you can use:

```bash
docker swarm init --advertise-addr
```

to startup the docker swarm within a node that will be your master node or swarm *leader*. Atfer this finishes, it will print on screen the command to execute on the other nodes to finish setting up the network.

You can then use the swarm-deploy.yml file to deploy the stack:

```
docker stack deploy -c swarm-deploy sb-cloud-be
```

If you wish to use the telegram APIs, remember to export the TELEGRAM_KEY environment variable before launching THE STACK:

```bash
TELEGRAM_KEY="your bot token here" docker stack deploy -c swarm-backend.yml sb-cloud-be
```

## Edge and end device connection

The cloud layer is the last tier of the SB architecture. It is connected with the edge servers and some end devices via different means.

### Edge devices MQTT connection

Edge devices are connected to the cloud through MQTT. An MQTT broker is hosted on the cloud stack and is used to exchange sensor and actuation data with the edge layer devices.

The topic on which the cloud is subscribed is **/sensor/#**, and it expectes topics in the **/sensor/{roomid}/{datatype}**, like **/sensor/3/temperature**. After the data is processed and saved, the actuation MQTT messages are forwarded to the right edge device using the topic **/actuator/{roomid}/{devicename}**, where roomid is the code of the room tied to that edge device, while devicename identifies which device is being actuated.

### QR interface

Some HTTP APIs were designed with the intention of being called through a QR scanning mechanism. This is to make it easy for people to interact with them when entering in the environment.

## Room APIs 

You can monitor the state of a room variables via the room APIs, either directly querying them via HTTP or through the bot interface:

- query them via HTTP through the **/api/room/{roomid}/** endpoint, where roomid is a number.
- connect to the bot via telegram and use the **/get n** command, where n is the room id.

## Telegram notification system

Telegram is used to send notifications to people in a room that has the possibility of having an higher rate of covid spread. User data is obtained through the QR system and is then saved on an in-memory data store.

You have to use the **/start** command in order for the bot to send you notifications about the rooms, use **/end** to stop them.



## Possible improvements

This project is really a proof of concept, with some details missing from a real production system. The intention of the project was to show a possible architectural solution, but it can be improved by:

- Implementing the backend with a more robust and optimized language.
- Adding SSL certificates to make everything run under HTTPS.
- Using broker authentication and certificates.
- Adding a load balancer on top of the swarm orchestration routing system.
- Scaling the number of nodes, at least 3 mastes that don't execute codes should be needed to make the system robust.