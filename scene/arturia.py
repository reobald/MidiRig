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

class ArturiaNRPN():
    def __init__(self):
        self.MSB = 0
        self.LSB = 0
        self.DATA = 0
        self.msbIsSet = False
        self.lsbIsSet = False
        self.dataIsSet = False 
    
    def commit(self):
      pgm = self.DATA
      self.reset()
      return pgm

    def setMsb(self, msb):
      print "msb=%d" % (msb)
      self.MSB = msb
      self.msbIsSet = True
      
    def setLsb(self, lsb):
      print "lsb=%d" % (lsb)
      self.LSB = lsb
      self.lsbIsSet = True
      
    def setData(self, data):
      print "data=%d" % (data)
      self.DATA = data
      self.dataIsSet = True
      
    def reset(self):
      self.MSB=0
      self.LSB=0
      self.DATA=0
      self.msbIsSet = False
      self.lsbIsSet = False
      self.dataIsSet = False
      
    def msgIsValid(self, midievent):
        if midievent.type!=CTRL or midievent.data1 not in [99,98,38,6]:
          return False
        
        if(midievent.data1==99 and not (self.lsbIsSet or self.dataIsSet)):
          return midievent.data2==0

        if(midievent.data1==98 and self.msbIsSet and not self.dataIsSet):
          return midievent.data2==0

        if(midievent.data1==38 and self.msbIsSet and self.lsbIsSet):
          return True
        
        if(midievent.data1==6 and self.msbIsSet and self.lsbIsSet and self.dataIsSet):
          return midievent.data2==127
          
        return False
        


#    def ProcessNRPN(self, midievent):
#      if self.msgIsValid(midievent):
#        if midievent.data1 == 99:
#          self.reset()
#          self.setMsb( midievent.data2 )
#        elif midievent.data1 == 98:
#          self.setLsb(midievent.data2)
#        elif midievent.data1 == 38:
#          self.setData(midievent.data2)
#        elif midievent.data1==6:
#          switchscene = self.commit();
#	  return [midievent,switchscene]
	  	
#      return midievent

#arturia = None

#def ProcessNRPNpgc(midievent):
#  if arturia==None:
#    arturia = ArturiaNRPN() 
#  
#  if arturia.msgIsValid(midievent):
#    if midievent.data1 == 99:
#      arturia.reset()
#      arturia.setMsb( midievent.data2 )
#    elif midievent.data1 == 98:
#      arturia.setLsb(midievent.data2)
#    elif midievent.data1 == 38:
#      arturia.setData(midievent.data2)
#    elif midievent.data1==6:
#      pgm = arturia.commit();
#      return [midievent,SceneSwitch(pgm)]
	  	
#  return midievent
