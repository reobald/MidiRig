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


from mididings.event import MidiEvent,ProgramEvent,CtrlEvent
from mididings import *
import sys

class ArturiaMapping:
  def __init__(self):
    self.toggleMemory = {}
    self.MMC_rewind  = str((0xF0,0x7F,0x7F,0x06,0x05,0xF7))
    self.MMC_forward = str((0xF0,0x7F,0x7F,0x06,0x04,0xF7))
    self.MMC_stop    = str((0xF0,0x7F,0x7F,0x06,0x01,0xF7))
    self.MMC_play    = str((0xF0,0x7F,0x7F,0x06,0x02,0xF7))
    self.MMC_recStr  = str((0xF0,0x7F,0x7F,0x06,0x06,0xF7))

    self.transposeUp    = lambda: sys.stdout.write("transposeUp")
    self.transposeDown  = lambda: sys.stdout.write("transposeDown")
    self.transposeReset = lambda: sys.stdout.write("transposeReset")

    self.sysexMap = {
#      self.MMC_rewind:  lambda evt: self.transposeDown(),
#      self.MMC_forward: lambda evt: self.transposeUp(),
#      self.MMC_stop: 	lambda evt: self.transposeReset(),
#      self.MMC_recStr:  lambda evt: Panic()
    }

    self.ctrlMap = {
      12: lambda evt: CtrlEvent(evt.port,16,82,evt.value),
      22: lambda evt: self.convertCtlToPgm(evt,1),
      23: lambda evt: self.convertCtlToPgm(evt,2),
      24: lambda evt: self.convertCtlToPgm(evt,3),
      25: lambda evt: self.convertCtlToPgm(evt,4),
      26: lambda evt: self.convertCtlToPgm(evt,5),
      27: lambda evt: self.convertCtlToPgm(evt,6),
      28: lambda evt: self.convertCtlToPgm(evt,7),
      29: lambda evt: self.convertCtlToPgm(evt,8),
      30: lambda evt: self.convertCtlToPgm(evt,15),
      31: lambda evt: self.convertCtlToPgm(evt,16),
      53: lambda evt: self.transposeDown(),
      52: lambda evt: self.transposeUp(),
      51: lambda evt: self.transposeReset(),
#      54: lambda evt: CtrlEvent(evt.port,16,82,evt.value),
#      50: lambda evt: CtrlEvent(evt.port,16,82,evt.value),
      55: lambda evt: self.toggleCtrl(CtrlEvent(evt.port,16,82,evt.value)),
      64: lambda evt: CtrlEvent(evt.port,evt.channel,64,127-evt.value),
    }


  def returnMapping(self,midiEvent):
    try:
	if midiEvent.type==CTRL:
	   return  self.ctrlMap[midiEvent.ctrl](midiEvent)
	elif midiEvent.type == SYSEX:
	   sysexKey = str(midiEvent.sysex)
	   return self.sysexMap[sysexKey]
    except KeyError:
	pass
    return midiEvent


  def convertCtlToPgm(self,midiEvent,program):
	if midiEvent.value>0:
	   port = midiEvent.port
	   channel = midiEvent.channel
	   return ProgramEvent(port, channel, program)
	return None

  def registerTransposeUp(self, f):
	self.transposeUp = f	
	
  def registerTransposeDown(self, f):
	self.transposeDown = f	

  def registerTransposeReset(self, f):
	self.transposeReset = f	


  def toggleCtrl(self, midiEvent):
	if midiEvent.value>0:
	   toggle = self.toggleMemory.get(midiEvent.ctrl,True)
	   midiEvent.value = toggle*midiEvent.value
	   self.toggleMemory[midiEvent.ctrl]= not toggle
	   return midiEvent
	return None


