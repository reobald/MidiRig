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

class Integra7Sysex():
    def __init__(self, ID=0x10):
        #Sysex base message
        self.BASE = [0xf0, 0x41, ID, 0x00, 0x00, 0x64]

    def checksum(self,bytes):
        sum = 0
        csum = 0
        for i in bytes:
                csum = csum+i
        sum = sum & 0x7f
        csum = ~sum & 0x7f
        return [csum]

    def appendSpace(self, input):
        l = 16 - len(input)
        for i in range(l):
                input = input + " "
        return input
        
    def generateNameMsg(self, name):
        cmd = [0x12]
        address = [0x18,0x00,0x00,0x00]
        name = self.appendSpace(name)
        msg = address + map(ord,name)
        end = [0xf7]
        csum = self.checksum(msg)
        return self.BASE + cmd + msg + csum + end

    def generateChannelChangeMsg(self, part, channel):
	part = part -1
	channel = channel -1
	partAddress = 0x20 + part
	channelParameterAddress = 0x00

        cmd = [0x12]
        address = [0x18,0x00,partAddress,channelParameterAddress]
        msg = address + [channel]
        end = [0xf7]
        csum = self.checksum(msg)
        return self.BASE + cmd + msg + csum + end

    def generateVolumeChangeMsg(self, part, volume):
	part = part -1
	partAddress = 0x20 + part
	volumeParameterAddress = 0x09

        cmd = [0x12]
        address = [0x18,0x00, partAddress, volumeParameterAddress]
        msg = address + [volume]
        end = [0xf7]
        csum = self.checksum(msg)
        return self.BASE + cmd + msg + csum + end

    def generateTransposeMsg(self,transpose):
	#F0H Exclusive status
	#7FH ID number (universal realtime message) 7FH Device ID (Broadcast)
	#04H Sub ID#1 (Device Control)
	#04H Sub ID#2 (Master Coarse Tuning)
	#llH Master Coarse Tuning LSB
	#mmH Master Coarse Tuning MSB
	#F7H EOX (End Of Exclusive)
	#llH: ignored (processed as 00H)
	#mmH: 28H - 40H - 58H (-24 - 0 - +24 [semitones])
        return [0xf0, 0x7f, 0x04, 0x04, 0x00, transpose, f7]
	



