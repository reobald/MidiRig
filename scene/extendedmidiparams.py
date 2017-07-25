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

from mididings import *
from mididings.event import MidiEvent
from mididings.units.call import Process
from mididings.extra.osc import SendOSC

class NRPNMidiEvent(MidiEvent):
    def __init__(self, event, nrpnctrl):
        super(NRPNMidiEvent,self).__init__(event.type,
					   port=event.port,
					   data1=event.data1,
					   data2=event.data2,
					   sysex=event.sysex)
	self.nrpnctrl = nrpnctrl

class MidiNRPNTransaction():
    def __init__(self):
	self.MSB = 0
	self.LSB = 0
		    
    def storeAndHandle(self, midievent):
	try:
	   ctrl = midievent.ctrl
	   value = midievent.value
	   if (ctrl == 99):
		self.MSB = value
	   elif (ctrl == 98):
		self.LSB = value
	   elif (ctrl == 38):
		self.__init__()
		nrpnctrl = self.getExtendCtrlNr(midievent)
	        return NRPNMidiEvent(midievent,nrpnctrl)
	except:
	   return None
	return None
	
    def getExtendCtrlNr(self,midievent):
	extendedCtrl = self.MSB<<8
	extendedCtrl += self.LSB
	return extendedCtrl

	
#global variables
CTRL_BROWSE_SCENE = (127<<8) + 126
CTRL_CHANGE_SCENE = (127<<8) + 127
CTRL_TRANSPOSE = (127<<8) + 125
midinrpn = MidiNRPNTransaction()
browsedScene = 0
transposeOffset = 0

#supporting functions
def nrpn(midievent):
	return midinrpn.storeAndHandle(midievent)

def saveBrowsedScene(midievent):
	browsedScene = midievent.data2
	return midievent

def setGlobalTransposeOffset(midievent):
	value = midievent.value
	if value==64:
		transposeOffset = 0
	elif value>64:
		transposeOffset+=1
	else:
		transposeOffset-=1

def getTransposeEditMessage(midievent):
	text = "**** EDIT **** "
	text += "Transpose: "
	text += str(transposeOffset)
	return text

def nrpnFilter(midievent,nrpnctrl):
	try:
		if midievent.nrpnctrl==nrpnctrl:
		   return midievent
	except:
		return None
	return None


def nrpnBrowseSceneFilter(midievent):
	return nrpnFilter(midievent,CTRL_BROWSE_SCENE)

def nrpnChangeSceneFilter(midievent):
	return nrpnFilter(midievent,CTRL_CHANGE_SCENE)

def nrpnTransposeFilter(midievent):
	return nrpnFilter(midievent,CTRL_TRANSPOSE)


#mididings extensions
def HandleNRPN():
	return Process(nrpn)

def BrowseScene():
	return Process(nrpnBrowseSceneFilter) >> Process(saveBrowsedScene)>>SendOSC(56419,'/system/preview/scene',browsedScene)>>Discard()

def ChangeScene():
	return Process(nrpnChangeSceneFilter) >>  CtrlValueFilter(127) >> SceneSwitch(browsedScene)>>Discard()

def SetGlobalTransposeOffset():
	return Process(nrpnTransposeFilter) >> Process(setGlobalTransposeOffset) >> SendOSC(56419,'/system/preview/text',getTransposeEditMessage())>>Discard()

def GlobalTranspose():
	return Transpose(transposeOffset)

	

