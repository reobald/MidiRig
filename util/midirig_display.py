#!/usr/bin/python

# Copyright (C) 2015-2017 Patrik Jonasson - All Rights Reserved 
#
#
# This file is part of MidiRig.
#
# MidiRig is free software: you can redistribute it and/or modify it  
# under the terms of the GNU General Public License as published by  
# the Free Software Foundation, either version 3 of the License,  
# or (at your option) any later version. 
#
# MidiRig is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY;
# without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOS$
# See the GNU General Public License for more details. 
#
# You should have received a copy of the GNU General Public License along with MidiRig.
# If not, see <http://www.gnu.org licenses/>. 

import liblo, sys, smbus, time, signal, threading, subprocess
from previewer import Previewer
from arturia_sysex import ArturiaSysexTransmitter

#mididings global variables
data_offset = 0
scenes = {}
tmp_scenes = {}
currentScene = 0

#I2C
i2cbus = smbus.SMBus(1)
i2caddress = 0x04	

# Midirig display commands
UPDATE_SEVEN_SEG_NUMBER = 0
UPDATE_LCD_ROW1 = 1
UPDATE_LCD_ROW2 = 2
CLEAR_LCD = 3
UPDATE_SEVEN_SEG_TEXT = 4

ACK = 0
ERR = 1

# constants
ROW1 = 0
ROW2 = 1
ALL = 2

#Arturia display
sysex_trx = ArturiaSysexTransmitter()
sysex_trx.start()

def updateArturiaDisplay(lcd_text):
	sysex_trx.sendText(lcd_text)

def i2cWriteString(cmd,str):
	datalist = map( ord, str)
	i2cbus.write_i2c_block_data(i2caddress,cmd,datalist)
	print("Raspberry pi: {0}, {1}, {2}".format(i2caddress,cmd,datalist))

def i2cWriteByte(cmd,value):
	i2cbus.write_byte_data(i2caddress,cmd,value)
	print("Raspberry pi: {0}, {1}, {2}".format(i2caddress,cmd,value))

def i2cWriteBytes(cmd,bytes):
        i2cbus.write_i2c_block_data(i2caddress,cmd,bytes)
        print("Raspberry pi: {0}, {1}, {2}".format(i2caddress,cmd,bytes))

def toBytes(input):
	byte1 = input & 255
	byte2 = input>>8
	return [byte1,byte2]

def i2cWaitForAck():
	for i in range(100):
		time.sleep(0.001)
		result = i2cbus.read_byte(i2caddress)
		if result==ACK:
			print("Arduino     : ACK")
			return True
		if result==ERR:
			print("Arduino     : ERR")
			return False
	print("Arduino     : Timeout")
	return False
	
def splitIntoTwoRows(st):
	st = st.strip();
	if len(st)<=16:
		return [st,""]
		
	i = st[0:17].rfind(' ')
	if i==-1:
		return [st,""]
		
	return [st[0:i].strip(),st[i:].strip()]

def getSceneName(sceneNumber):
	global scenes
	try:
	   sceneInfo = scenes[sceneNumber]
	   name = sceneInfo[0]
	except KeyError:
	   name = "Unknown"
	return name
	

def update7SegNumber(sceneNumber):
	bytes = toBytes(sceneNumber)
   	i2cWriteBytes(UPDATE_SEVEN_SEG_NUMBER,bytes)
   	if not i2cWaitForAck():
      		return

def update7SegText(txt):
   	i2cWriteString(UPDATE_SEVEN_SEG_TEXT,txt)
   	if not i2cWaitForAck():
      		return


def updateDisplayMsg(inputText):
	dividedText = splitIntoTwoRows(inputText)

	i2cWriteByte(CLEAR_LCD,ALL)
	if not i2cWaitForAck():
      		return
   	i2cWriteString(UPDATE_LCD_ROW1, dividedText[ROW1])
   	if not i2cWaitForAck():
      		return
   	i2cWriteString(UPDATE_LCD_ROW2, dividedText[ROW2])
   	if not i2cWaitForAck():
      		return



lock = threading.Lock()
def updateDisplay(sevseg_info, lcd_text):
    print "updateDisplay: {}".format(lcd_text)
    try:
	lock.acquire()
	try:
   	   update7SegNumber(sevseg_info)
   	except TypeError:
   	   update7SegText(sevseg_info)
	updateDisplayMsg(lcd_text)
#	arturia_msg = "{:0>3}: {}".format(sevseg_info, lcd_text)
	arturia_msg = "{}: {}".format(sevseg_info, lcd_text)
	updateArturiaDisplay(arturia_msg)
    finally:
	lock.release()

# create server, listening on port 56419
try:
    server = liblo.Server(56419)
except liblo.ServerError as err:
    print(err)
    sys.exit()

previewer = Previewer(updateDisplay)
previewer.start()

#create handler for graceful exit
def handler(signum, frame):
    previewer.stop_event.set()
    sysex_trx.stop()
    print 'Exiting midirig_display'
    sys.exit()

#attach handler to system signals
signal.signal(signal.SIGTERM, handler)
signal.signal(signal.SIGINT, handler)

#('/mididings/data_offset', 'i')
def data_offset_cb(path, args):
    global data_offset
    data_offset = args[0]
    print(path, args)
server.add_method("/mididings/data_offset", 'i', data_offset_cb)


#('/mididings/begin_scenes', '')
def begin_scenes_cb(path, args):
   global tmp_scenes
   tmp_scenes = {}
   print(path, args)
server.add_method("/mididings/begin_scenes", '', begin_scenes_cb)

#('/mididings/add_scene', None)
def add_scene_cb(path, args):
   global tmp_scenes
   number, name = args[:2]
   print(number)
   subscenes = args[2:]
   tmp_scenes[number] = (name, subscenes)
   print(path, args)   
server.add_method("/mididings/add_scene", None, add_scene_cb)

#('/mididings/end_scenes', '')
def end_scenes_cb(path, args):
   global scenes
   global tmp_scenes
   scenes = tmp_scenes
   print(path, args)
server.add_method("/mididings/end_scenes", '', end_scenes_cb)

#('/mididings/current_scene', 'ii')
def current_scene_cb(path, args):
   previewer.cancelPreview()
   global currentScene
   currentScene = args[0]
   sceneName = getSceneName(currentScene)
   updateDisplay(currentScene,sceneName)
   print(path, args)
server.add_method("/mididings/current_scene", 'ii', current_scene_cb)

#('/system/preview/scene', 'i')
def system_preview_scene_cb(path, args):
   print(path, args)
   previewLed = args[0]
   previewLcd = getSceneName(previewLed)
   origLed = currentScene
   origLcd = getSceneName(currentScene)
   previewer.preview(origLed,origLcd, previewLed, previewLcd)
server.add_method("/system/preview/scene", 'i', system_preview_scene_cb)

#('/system/preview/text', 's')
def system_preview_text_cb(path, args):
   print(path, args)
   previewLed = "   "
   previewLcd = args[0]
   origLed = currentScene
   origLcd = getSceneName(currentScene)
   previewer.preview(origLed,origLcd, previewLed, previewLcd)
server.add_method("/system/preview/text", 's', system_preview_text_cb)

#('/system/msg', 's')
def system_msg_cb(path, args):
   updateDisplay("---",args[0])
   print(path, args)   
server.add_method("/system/msg", 's', system_msg_cb)



#Fallback method
def fallback(path, args, types, src):
    print("got unknown message '%s' from '%s'" % (path, src.url))
    for a, t in zip(args, types):
        print("argument of type '%s': %s" % (t, a))
server.add_method(None, None, fallback)



# loop and dispatch messages every 100ms
print("Server listening at port 56419")
while True:
    server.recv(100)















