#!/usr/bin/python
# -*- coding: utf-8 -*-

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
# without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.   
# See the GNU General Public License for more details. 
#
# You should have received a copy of the GNU General Public License along with MidiRig.
# If not, see <http://www.gnu.org licenses/>. 


import sys
import signal
#from arturia import ArturiaNRPN
from mididings import *
from mididings.extra.gm import *
from mididings.extra.osc import OSCInterface
from mididings.extra.osc import SendOSC
from mididings.extra import *
from mididings.event import NoteOffEvent,CtrlEvent
from blinkingled import BlinkingLed
from scene import *
from channelmapping import ChannelMapping
from arturiamapping import ArturiaMapping
#=================================
# setup midiactivity indicator led
#=================================
MIDIACTIVITY_LED_PIN = 25

led = BlinkingLed(MIDIACTIVITY_LED_PIN)
led.start()

# the method that gets called at a midi event
def midiactivity(midiEvent):
	led.blink()
	return midiEvent

#create handler for graceful exit
def handler(signum, frame):
    led.stop_event.set()
    print 'Exiting MidiRig'
    sys.exit()

#attachhandler to system signals
signal.signal(signal.SIGTERM, handler)
signal.signal(signal.SIGINT, handler)



#=================================
# Configure MIDI environment
#=================================
config(
    # use ALSA as backend
    backend='alsa',
    # set ALSA client name
    client_name='MidiRig',
    #name ports and connect them to alsa client
    in_ports = [
      ('default in', 'Virtual Raw MIDI 0-0.*:0'),
      ('KeyLab_in',    'KeyLab.*:0'),
      ('INTEGRA-7_in',    'INTEGRA-7.*:0'),
      ('MidiRigDisplay_in',  'MidiRigDisplay.*:0')
    ],
    out_ports=[
      #('KeyLab_out',    'KeyLab.*:0'),
      ('KeyLab_out',    'KeyLab 61.*:0'),
      ('INTEGRA-7_out',    'INTEGRA-7.*:0'),
    ],
    # ...or just change the number of ports available    #in_ports=2,

    # when using a patchbay like QjackCtl, a small delay allows ports to be
    # connected before any MIDI events are sent
    #start_delay=0.5,
)


#=================================
# Configure OSC communication
#=================================
port = sys.argv[1]
notify_ports = sys.argv[2:]
hook(
        OSCInterface(port,notify_ports)
)

#================================================
# Setup midi channel translation infrastructure
#================================================
chMap = ChannelMapping(lowerSourceCh=2,upperSourceCh=1)
TranslateChannel = Process(chMap.translateCh)
PgcChannelMapping = Process(chMap.pgcChannelMapping) 
ArturiaChannelMapping = Process(chMap.arturiaChannelMapping)
RegNoteOn = Process(chMap.regNoteOn)
HandleNoteOff = Process(chMap.handleNoteOff)
RegSusOn = Process(chMap.regSusOn)
HandleSustainOff = Process(chMap.handleSustainOff)

#================================================
# Setup arturia controller number mappings
#================================================
oscPort = sys.argv[2]
oscPrevAddr = "/system/preview/scene"
arturiaMap = ArturiaMapping()
Arturia = (SysExFilter(manufacturer=(0x00,0x20,0x6B)) | ChannelFilter(1)) % \
	  (Process(arturiaMap.returnMapping)>> \
          CtrlFilter( arturiaMap.presetCtrlNr) % \
		(SceneSwitch(number=EVENT_DATA2)>>Discard()) >> \
          CtrlFilter( arturiaMap.browseCtrlNr) % \
		(SendOSC(oscPort,oscPrevAddr,lambda evt: evt.data2)>>Discard())\
	  )
#================================================
# All notes off - because ctrl 123 is not implemented by nord
# and also a all notes off message should send note off on all channels
# not only one channel
#================================================
def allNotesOff(midievent):
   if midievent.type==CTRL and midievent.ctrl==123:
      allnotesoff = []
      for ch in range(1,17):
	allnotesoff.append(CtrlEvent(midievent.port,ch,123,0))
      for ch in range(15,17):
         for note in range(29,102):
	    allnotesoff.append(NoteOffEvent(midievent.port,ch,note,0))
         allnotesoff.append(CtrlEvent(midievent.port,ch,64,0))
      return allnotesoff
   return midievent	


#================================================
# Setup transpose infrastructure
#================================================
transpose = 0
def setTranspose(midievent):
	global transpose 
	transpose = midievent.sysex[5]-64
	return midievent

def globalTranspose(midievent):
	midievent.note += transpose
	if 0 <= midievent.note <= 127: 
	   return midievent
	else: 
	   return None

def transposeMsg(midievent):
	global transpose
	return "**** EDIT **** Transpose {}".format( transpose )


SetTranspose = SysExFilter([0xf0, 0x7f, 0x04, 0x04, 0x00]) \
		% (Process(setTranspose) \
		>> [SendOSC(56419, "/system/preview/text", lambda e: transposeMsg(e) ) \
		, Ctrl(123, 0)] )
GlobalTranspose = Filter(NOTE) % Process(globalTranspose)


# cc82 always on ch 16
cc82ch16 = CtrlFilter(82) % Channel(16)

# PRE: signal midiactivity, perform arturia controller mappings and channelmappings
pre     = Print("pre") \
		>> Process(midiactivity) >> Arturia >> Print("in")  \
		>> PgcChannelMapping >> ArturiaChannelMapping >> TranslateChannel  \
		>> RegNoteOn >> RegSusOn >> HandleNoteOff >> HandleSustainOff  \
		>> cc82ch16 >> SetTranspose >> GlobalTranspose >> Process(allNotesOff)

# CONTROL: select only program changes
#control	= Filter(PROGRAM)
control	= Discard()

#POST    : log and redirect to a port
post	= Print("out")  \
		>> [SysExFilter(manufacturer=(0x00,0x20,0x6B))  \
			%Port('KeyLab_out'),Port('INTEGRA-7_out')]



#######################################################
# Scenes section
#######################################################
run(
    scenes = {
	1  :    scene001.config(),
	2  :    scene002.config(),
	3  :    scene003.config(),
	4  :    scene004.config(),
	5  :    scene005.config(),
	6  :    scene006.config(),
	7  :    scene007.config(),
	8  :    scene008.config(),
	9  :    scene009.config(),
	10 :    scene010.config(),
	11 :    scene011.config(),
	12 :    scene012.config(),
	13 :    scene013.config(),
	14 :    scene014.config(),
	15 :    scene015.config(),
	16 :    scene016.config(),
	17 :    scene017.config(),
	18 :    scene018.config(),
	19 :    scene019.config(),
	20 :    scene020.config(),
	21 :    scene021.config(),
	22 :    scene022.config(),
	23 :    scene023.config(),
	24 :    scene024.config(),
	25 :    scene025.config(),
	26 :    scene026.config(),
	27 :    scene027.config(),
	28 :    scene028.config(),
	29 :    scene029.config(),
	30 :    scene030.config(),
	31 :    scene031.config(),
	32 :    scene032.config(),
	33 :    scene033.config(),
	34 :    scene034.config(),
	35 :    scene035.config(),
	36 :    scene036.config(),
	37 :    scene037.config(),
	38 :    scene038.config(),
	39 :    scene039.config(),
	40 :    scene040.config(),
	41 :    scene041.config(),
	42 :    scene042.config(),
	43 :    scene043.config(),
	44 :    scene044.config(),
	45 :    scene045.config(),
	46 :    scene046.config(),
	47 :    scene047.config(),
	48 :    scene048.config(),
	49 :    scene049.config(),
	50 :    scene050.config(),
	51 :    scene051.config(),
	52 :    scene052.config(),
	53 :    scene053.config(),
	54 :    scene054.config(),
	55 :    scene055.config(),
	56 :    scene056.config(),
	57 :    scene057.config(),
	58 :    scene058.config(),
	59 :    scene059.config(),
	60 :    scene060.config(),
	61 :    scene061.config(),
	62 :    scene062.config(),
	63 :    scene063.config(),
	64 :    scene064.config(),
	65 :    scene065.config(),
	66 :    scene066.config(),
	67 :    scene067.config(),
	68 :    scene068.config(),
	69 :    scene069.config(),
	70 :    scene070.config(),
	71 :    scene071.config(),
    },
    control = control,
    pre = pre,
    post = post
)
