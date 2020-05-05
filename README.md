# Tcp Chat App

![python:3.8](https://img.shields.io/badge/python-3.8-blue)
![tornado:6.0.4](https://img.shields.io/badge/tornado-6.0.4-orange)
![asyncio:3.4.3](https://img.shields.io/badge/asyncio-3.4.3-blueviolet)
![build:passing](https://img.shields.io/badge/build-passing-green)

A simple Tcp chat app for multiple humans(or robots, depending on where your priorities are) that uses 
```tornado.websockets.WebsocketHandler``` which  allows for bidirectional communication between the browser and server.

```tornado.websockets.WebsocketHandler``` implements the final version of the WebSocket protocol as defined in RFC 6455. 
Certain browser versions (notably Safari 5.x) implemented an earlier draft of the protocol (known as “draft 76”) 
and are not compatible with this module.
Read the docs [here](https://www.tornadoweb.org/en/stable/websocket.html)


## Requirements

- Python 3.7+ 

    - [download](https://www.python.org/downloads/)
    
    - [documentation](https://docs.python.org/3/)

- Tornado 
   ```
   pip install Tornado
   ```
    - [documentation](https://www.tornadoweb.org/en/stable/)



## Demo

 Here's a screen recording showing multiple clients(2 clients chatting with each other inreal time). I made it so that the server can handle 30 connections.
 
![demo](https://user-images.githubusercontent.com/39020723/81034191-000cbb00-8e9f-11ea-9999-3cdbe37da8de.gif)


