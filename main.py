__author__ = "Donat Marko"
__copyright__ = "2018 Donat Marko | www.donatus.hu"
__credits__ = ["Donat Marko"]
__license__ = "GPL-3.0"

import serial
import time
import sys
import json
import bottle
import time
from config import *

# Array that stores the relays' statuses
relaystates=[False, False, False, False, False, False, False, False]
print("DonatuSoft HTTP middleware for KMTronic USB relay boxes. www.donatus.hu. 2018.")

# As Bottle is asynchronous, we have to connect to the COM port on-demand.
def serialconnect(): 
	ser=serial.Serial()
	try:
		ser = serial.Serial(serial_port)
		print("Opening " + ser.name + ".")
	except:
		print("Unable to open the given serial port. Maybe you are not admin/root (and you'd need to be)")
	return ser

# We need to reset the relays (i.e. switch them off) upon startup as the module does NOT store (neither return) the states.
def relayinit():
	ser=serialconnect()
	ser.write(serial.to_bytes([0xFF,0x00,0x00]))
	print("Relays reset.")
	
# Root page
@bottle.route('/')
def info():
	bottle.response.content_type="text/text"
	return '''
		Hello World!
		
		This is DonatuSoft HTTP middleware for KMTronic USB relay boxes.
		
		---------------------------------------------------------------------------------------------------------------------------------------
		 USAGE:
		---------------------------------------------------------------------------------------------------------------------------------------
		
			GET  /relays                              Returns the status of the relays in JSON format.
			GET  /relays/<nr>/on                      Turns the specified relay ON, returns JSON status.
			GET  /relays/<nr>/off                     Turns the specified relay OFF, returns JSON status.
			GET  /relays/<nr>/toggle                  Toggles the specified relay, returns JSON status.
			GET  /relays/<nr>                         Returns status of the specified relay as a single boolean.
			POST /relays/<nr>                         Turns ON or OFF the relay (whether body contains 'ON' or 'OFF' part)
					
		Upon startup the middleware RESETs all relays as the status can NOT be retrieved from the module itself! We store them internally.
		
		https://github.com/donatmarko/kmtronic-usb-relaybox-http
		www.donatus.hu
		2018
	'''

# JSON formatted summary
@bottle.route('/relays')
def index():
	bottle.response.content_type="application/json"
	jsonstates=dict()
	for i, state in enumerate(relaystates, start=1):
		jsonstates["R" + str(i)]=state
	return json.dumps(jsonstates)

# We do not accept any operations on 0th relay = address reserver by KMTronic for all relays.
@bottle.route('/relays/0/toggle')
@bottle.route('/relays/0/on')
@bottle.route('/relays/0/off')
def illegaloperation():
	bottle.response.content_type="application/json"
	return '{"error":"Illegal Operation"}'
	
# Returns state as boolean of single relays
@bottle.route('/relays/<relay>', method='GET')
def relaybool(relay):
	relay=int(relay)
	return "ON" if relaystates[relay-1] else "OFF"

# Relay operations through POST request
@bottle.route('/relays/<relay>', method='POST')
def post(relay):
	for l in bottle.request.body:
		if "ON" in str(l):
			on(relay)
		if "OFF" in str(l):
			off(relay)
		if "TOGGLE" in str(l):
			toggle(relay)

# Relay operations through GET request
@bottle.route('/relays/<relay>/on')
def on(relay):
	relay=int(relay)
	serialconnect().write(serial.to_bytes([0xFF,relay,0x01]))
	time.sleep(0.05)
	relaystates[relay-1]=True
	return index()
	
@bottle.route('/relays/<relay>/off')
def off(relay):
	relay=int(relay)
	serialconnect().write(serial.to_bytes([0xFF,relay,0x00]))
	time.sleep(0.05)
	relaystates[relay-1]=False
	return index()
	
@bottle.route('/relays/<relay>/toggle')
def toggle(relay):
	relay=int(relay)
	relaystates[relay-1]=not(relaystates[relay-1])
	serialconnect().write(serial.to_bytes([0xFF,relay, 0x01 if relaystates[relay-1] else 0x00 ]))
	time.sleep(0.05)
	return index()

# Core functions
try:
	relayinit()
	bottle.run(host='0.0.0.0', port=web_port)
except KeyboardInterrupt:
	quit()