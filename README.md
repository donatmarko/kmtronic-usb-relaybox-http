# HTTP middleware for KMTronic USB relay boxes
> Python3 middleware for KMTronic USB 8 channel relay boxes to control the relays remotely with HTTP requests.

## What is it for?
This middleware has been developed for the **KMTronic USB Relay Controller Eight Channel** model to control the relays remotely and to make it controllable by various home automation systems, such as Home-Assistant.

It contains a lightweight web-server (based on Bottle) and makes it possible to turn on/off the relays with simple HTTP GET and POST requests. 

## Installation and running
1. Install the requirements:
   `python -m pip install -r requirements.txt`
2. Run the middleware with specifying the COM and TCP ports:
   `python -m main.py COM8 8000`
   `python -m main.py /dev/ttyACM0 8000`
3. Done :)

## Commands
Method | URI                 | Content-Type     | Purpose
------ | ------------------- | ---------------- | ------------------------------
GET    | /                   | text/text        | General info how the API works
GET    | /relays             | application/json | Status of all relays in JSON format
GET    | /relays/{id}        | text/text        | Status of one specific relay (ON/OFF)
GET    | /relays/{id}/on     | application/json | Turns ON the relay and returns output of /relays
GET    | /relays/{id}/off    | application/json | Turns OFF the relay and returns output of /relays
GET    | /relays/{id}/toggle | application/json | TOGGLEs the relay and returns output of /relays
POST   | /relays/{id}        | text/text        | Turns ON or OFF (depending on the body) the relay and returns output of /relays/{id} - ***ideal for Home-Assistant RESTful switches***

## Bugreport, feature request?
Create a new issue at GitHub and I will do my best with.

## Warranty?
No.