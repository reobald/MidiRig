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
# without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOS$
# See the GNU General Public License for more details. 
#
# You should have received a copy of the GNU General Public License along with MidiRig.
# If not, see <http://www.gnu.org licenses/>. 


from mididings.event import MidiEvent,ProgramEvent,CtrlEvent,SysExEvent
from mididings import *
from mididings.extra.osc import SendOSC
import sys

class ArturiaMapping:
  def __init__(self):
    self.transpose = 0
    self.preset = 1

    self.resetDisplayEvent = None
   
    self.toggleMemory = {}

    self.browseCtrlNr = 114
    self.presetCtrlNr = 115


    self.ctrlMap = {
      12:  lambda evt: CtrlEvent(evt.port,16,82,evt.value),
      22:  lambda evt: self.convertCtlToPgm(evt,1),
      23:  lambda evt: self.convertCtlToPgm(evt,2),
      24:  lambda evt: self.convertCtlToPgm(evt,3),
      25:  lambda evt: self.convertCtlToPgm(evt,4),
      26:  lambda evt: self.convertCtlToPgm(evt,5),
      27:  lambda evt: self.convertCtlToPgm(evt,6),
      28:  lambda evt: self.convertCtlToPgm(evt,7),
      29:  lambda evt: self.convertCtlToPgm(evt,8),
      30:  lambda evt: self.convertCtlToPgm(evt,15),
      31:  lambda evt: self.convertCtlToPgm(evt,16),
      53:  lambda evt: self.transposeSysex(evt,-1),
      52:  lambda evt: self.transposeSysex(evt,1),
      51:  lambda evt: self.transposeSysex(evt,0),
#      54:  lambda evt: CtrlEvent(evt.port,16,82,evt.value),
#      50:  lambda evt: CtrlEvent(evt.port,16,82,evt.value),
      55:  lambda evt: self.toggleCtrl(CtrlEvent(evt.port,16,82,evt.value)),
      64:  lambda evt: CtrlEvent(evt.port,evt.channel,64,127-evt.value),
      114: lambda evt: self.browsePresets(evt),
      115: lambda evt: self.selectPreset(evt),
      118: lambda evt: self.stepPreset(evt,0),
      119: lambda evt: self.stepPreset(evt,127),
    }



  def returnMapping(self,midiEvent):
    try:
	if midiEvent.type==CTRL:
	   return  self.ctrlMap[midiEvent.ctrl](midiEvent)
    except KeyError:
    	pass
    if self.isArturiaSysexNameMsg(midiEvent):
	self.resetDisplayEvent = midiEvent
    return midiEvent

  def toggleButtonLights(self, event):
	button = event.ctrl-22
	event_list = []
	for i in range(10):
	  btn_adr = 0x12 + i
	  btn_value = 127 * (i == button)
	  cmd = [0xF0,0x00,0x20,0x6B,0x7F,0x42,0x02,0x00,0x10,btn_adr,btn_value,0xF7]
          event_list.append(SysExEvent(event.port,cmd))
	return event_list
	  

  def convertCtlToPgm(self,midiEvent,program):
	if midiEvent.value>0:
	   port = midiEvent.port
	   channel = midiEvent.channel
	   return ProgramEvent(port, channel, program)
	else:
	   sysex_events = self.toggleButtonLights(midiEvent)
	   sysex_events.append(self.resetDisplayEvent)
	   return sysex_events


  def toggleCtrl(self, midiEvent):
	if midiEvent.value>0:
	   toggle = self.toggleMemory.get(midiEvent.ctrl,True)
	   midiEvent.value = toggle*midiEvent.value
	   self.toggleMemory[midiEvent.ctrl]= not toggle
	   return midiEvent
	return None

  def isArturiaSysexNameMsg(self,midiEvent):
	if midiEvent.type == SYSEX:
	   header = [0xf0, 0x00, 0x20, 0x6B, 0x7F, 0x42, 0x04, 0x00, 0x60]
	   for i,b in enumerate(header):
		if b != midiEvent.sysex[i]:
			print "no match: {}!={}".format(b,midiEvent.sysex[i])
			return False
	   return True
	else:
	   return False

  def browsePresets(self, midiEvent):
    if midiEvent.data2<64 and self.preset>1:
	self.preset-=1
    elif self.preset<256:
	self.preset+=1
    midiEvent.data2=self.preset
    return midiEvent

  def stepPreset(self, midiEvent,value):
    if midiEvent.data2>0:
	midiEvent.data1=114
        midiEvent.data2=value
	return self.browsePresets(midiEvent)
    else:
	return self.resetDisplayEvent

  def selectPreset(self, midiEvent):
    if midiEvent.data2 > 0:
	midiEvent.data2=self.preset-1
        return midiEvent
    else:
	return self.resetDisplayEvent

  def printSysex(self,midiEvent):
	for c in midiEvent.sysex:
	  print c,

  def transposeSysex(self, midievent,transposeValue):
	if midievent.value>0:
	   tmp = 0 if transposeValue == 0 else self.transpose + transposeValue
	   if 0<= tmp <= 127:
	      self.transpose = tmp
	      msgList = self.generateAllNotesOff(midievent.port)
	      syx = [0xf0, 0x7f, 0x04, 0x04, 0x00, self.transpose, 0xf7]
	      msgList.append(SysExEvent(midievent.port,syx))
	      return msgList
	return self.resetDisplayEvent

  def generateAllNotesOff(self, port):
	allNotesOff = []
	for channel in range(1,17):
	   allNotesOff.append(CtrlEvent(port, channel, 123, 0))
	return allNotesOff

