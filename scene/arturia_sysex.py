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

class ArturiaSysex():
    def __init__(self, ID=0x10):
        #Sysex base message
        self.arturiaId = [0x00, 0x20, 0x6B]
        self.BASE = [0xf0] + self.arturiaId + [0x7F,0x42,0x04,0x00,0x60]

    def appendSpace(self, input):
        l = 16 - len(input)
        for i in range(l):
                input = input + " "
        return input

    def generateNameMsg(self, name):
        two_row_name = self.splitIntoTwoRows(name)
        result = self.BASE;  
        rowNr = 0x01;
        for row in two_row_name:
          result.append(rowNr)
          row = self.appendSpace(row)
          row = map(ord, row)
          result+=row
          result.append(0x00)
          rowNr += 1;
        result.append( 0xf7 )
        return result

    def splitIntoTwoRows(self, st):
        st = st.strip();
        if len(st)<=16:
                return [st,""]

        i = st[0:17].rfind(' ')
        if i==-1:
                return [st,""]

        return [st[0:i].strip(),(st[i:].strip())[0:16]]
	



