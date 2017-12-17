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


from mididings.event import MidiEvent,NoteOffEvent,CtrlEvent
from mididings import *
class ChannelMapping:
  def __init__(self, **kwargs):
        self.lowerSourceCh = kwargs.get('lowerSourceCh')
        self.upperSourceCh = kwargs.get('upperSourceCh')
        self.lowerDestCh = kwargs.get('lowerSourceCh')
        self.upperDestCh = kwargs.get('upperSourceCh')
        self.currentChannel = kwargs.get('lowerSourceCh')
	self.upperKeysPressed = {}
  	self.lowerKeysPressed = {}
	self.lowerSustain = {}
	self.upperSustain = {}
    
  def translateCh(self, midiEvent):
    if (midiEvent.channel==self.upperSourceCh):
        midiEvent.channel=self.upperDestCh
    elif (midiEvent.channel==self.lowerSourceCh):
        midiEvent.channel=self.lowerDestCh
    return midiEvent
    
  def pgcChannelMapping(self, midiEvent):
    if (midiEvent.type==PROGRAM):
      ch = midiEvent.program % 8
      if (ch==0):
        ch=16
      if (ch==7):
        ch=15
      if(midiEvent.channel==self.lowerSourceCh):
        self.lowerDestCh = ch
      elif(midiEvent.channel==self.upperSourceCh):
        self.upperDestCh = ch
      return None
    return midiEvent

  def arturiaChannelMapping(self, midiEvent):
      if(midiEvent.channel==self.upperSourceCh):
         if (midiEvent.type==CTRL):
           if (22 <= midiEvent.ctrl <= 29):
              self.upperDestCh = midiEvent.ctrl-21
              return None
           elif (30 <= midiEvent.ctrl <= 31):
              self.upperDestCh = midiEvent.ctrl-15
              return None
      return midiEvent
    
  def regNoteOn(self,midiEvent):
      if midiEvent.type==NOTEON:
          sourceUpper = midiEvent.channel == self.upperDestCh
          sourceLower = midiEvent.channel == self.lowerDestCh
          if sourceLower:
              self.lowerKeysPressed[midiEvent.data1]=midiEvent.channel
          if sourceUpper:
              self.upperKeysPressed[midiEvent.data1]=midiEvent.channel
      return midiEvent

  def regSusOn(self,midiEvent):
      if midiEvent.type==CTRL and  midiEvent.ctrl==64 and midiEvent.data2>=64:
          sourceUpper = midiEvent.channel == self.upperDestCh
          sourceLower = midiEvent.channel == self.lowerDestCh
          if sourceLower:
              self.lowerSustain[midiEvent.data1]=midiEvent.channel
          if sourceUpper:
              self.upperSustain[midiEvent.data1]=midiEvent.channel
      return midiEvent
	
      
  def handleNoteOff(self, midiEvent):
      eventList = [midiEvent]
      if midiEvent.type==NOTEOFF:
          sourceUpper = midiEvent.channel == self.upperDestCh
          sourceLower = midiEvent.channel == self.lowerDestCh
          key = midiEvent.data1
	  port = midiEvent.port
          if sourceLower:
              try:
              	  ch = self.lowerKeysPressed.get(key)
              	  eventList.append(MidiEvent(NOTEOFF,port,ch,key))
                  del self.lowerKeysPressed[key]
              except:
                  print "No previous lower key press registered"
          if sourceUpper:
              try:
              	  ch = self.upperKeysPressed.get(key)
              	  midiEvent.channel = ch
              	  eventList.append(MidiEvent(NOTEOFF,port,ch,key))
                  del self.upperKeysPressed[key]
              except:
                  print "No previous upper key press registered"
      return eventList

  def handleSustainOff(self, midiEvent):
      eventList = [midiEvent]
      if midiEvent.type==CTRL and midiEvent.ctrl==64 and midiEvent.data2<64:
          sourceUpper = midiEvent.channel == self.upperDestCh
          sourceLower = midiEvent.channel == self.lowerDestCh
          key = midiEvent.data1
	  port = midiEvent.port
          if sourceLower:
              try:
              	  ch = self.lowerSustain.get(key)
              	  eventList.append(MidiEvent(CTRL,port,ch,midiEvent.data1,midiEvent.data2))
                  del self.lowerSustain[key]
              except:
                  print "No previous sustain registered"
          if sourceUpper:
              try:
              	  ch = self.upperSustain.get(key)
              	  midiEvent.channel = ch
              	  eventList.append(MidiEvent(CTRL,port,ch,midiEvent.data1,midiEvent.data2))
                  del self.upperSustain[key]
              except:
                  print "No previous sustain registered"
      return eventList

