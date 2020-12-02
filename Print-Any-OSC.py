"""
Angelo Basteris - 18th November 2020 - angelobasteris@gmail.com
Simplest example OSC server

This program listens to the address/port specified and prints the received messages 
More info on OSC here: https://thewizardofosc.com/more-on-osc/

Apps for sending OSC messages from phone: oscHook, sensors2OSC, Osc Controller
"""
try:
	from pythonosc import osc_server,dispatcher
except:
	print("You need pythonosc (https://pypi.org/project/python-osc/) for this software. Install it with pip3 install python-osc.")
print("Python OSC server demo - angelobasteris@gmail.com\n")

## OSC server parameters
osc_address_pattern="/*"							## Change the string here if you want to react only to one specific address pattern
## Getting the IP address, in Linux and Windows
from sys import platform
if "linux" in platform:
	import os
	ip_address=os.popen('ip addr show wlp1s0 | grep "\<inet\>" | awk \'{ print $2 }\' | awk -F "/" \'{ print $1 }\'').read().strip()
if "win" in platform:
	try:
		import netifaces
	except:
		print("netifaces module missing - try to install it using pip3 install netifaces")
	netifaces.ifaddresses(netifaces.gateways()['default'][netifaces.AF_INET][1])[netifaces.AF_INET][0]['addr']
port=9000									## Choose any

def on_message_received(*args): 						## Our callback
	print(args)								## In this case only printing the arguments

dispatcher = dispatcher.Dispatcher()						## Create a dispatcher - you can create more than one for different address patterns
dispatcher.map(osc_address_pattern, on_message_received)
server = osc_server.ThreadingOSCUDPServer((ip_address,port), dispatcher)	## Create and start an OSC server with the attached dispatcher
print("Server listening on %s:%d for address pattern %s"%(ip_address,port,osc_address_pattern))
print("Start an OSC device or your phone OSC stream.")
server.serve_forever()
