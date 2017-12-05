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
import time
import threading
from pyalsa.alsaseq import *
from subprocess import check_output

class ArturiaSysex():
    #Sysex base message
    arturiaId = [0x00, 0x20, 0x6B]
    BASE = [0xf0] + arturiaId + [0x7F,0x42,0x04,0x00,0x60]
    
    def appendSpace(self, input):
        l = 16 - len(input)
        for i in range(l):
                input = input + " "
        return input

    def generateNameMsg(self, name):
        two_row_name = self.splitIntoTwoRows(name)
        result = list(self.BASE);  
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
	
    def generateNameMsgAsStr(self,name):
	bytes = self.generateNameMsg(name)
	return ' '.join('{:02x}'.format(x) for x in bytes)



class ArturiaSysexTransmitter(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.stop_event = threading.Event()
 	self.alsaseq = Sequencer(clientname="MidiRigDisplay")
	#self.alsaseq.clientname = "MidiRigDisplay"
	if not self.alsaseq:
	    print "Failed to create alsaseq.Sequenser()"
	self.sysexHelper = ArturiaSysex()
	self.portId = -1
	self.portId = self.alsaseq.create_simple_port(name='out', type=SEQ_PORT_TYPE_APPLICATION,  caps=SEQ_PORT_CAP_SUBS_READ | \
          												SEQ_PORT_CAP_READ | \
          												SEQ_PORT_CAP_WRITE | \
          												SEQ_PORT_CAP_SUBS_WRITE)

	print "portId {}".format(self.portId) 
	self.midirig = None
	self.midirig_display = None
	self.connected = self.connect()
	self.printConnections()

    def run(self):
        while not self.stop_event.is_set():
           time.sleep(0.1)
	   try:
		self.alsaseq.drain_output()
	   except SequencerError:
		pass      

    def getMidiRigAddress(self):
	out = check_output(["aconnect", "-o"])
	i = out.find('MidiRigDisplay_in')
	if i>-1:
   	    i -= 4
   	    portId = out[i:(i+3)].strip()
   	    i = out.find('MidiRig')
   	    i -= 6
   	    clientId = out[i:(i+3)].strip()
   	    return (int(clientId),int(portId))
	return None

    def getMidiRigDisplayAddress(self):
	address = self.alsaseq.clientname+":"+str(self.portId)
	return self.alsaseq.parse_address( address )

    def sendText(self,text):
	syx = self.sysexHelper.generateNameMsg(text)
	evt = self.createEvent(syx)
	self.alsaseq.output_event(evt)


    def createEvent(self, sysexdata):
	event = SeqEvent(SEQ_EVENT_SYSEX,SEQ_TIME_STAMP_REAL)
	event.set_data({'ext':sysexdata})
	return event

    def connect(self):
	try:
	    self.midirig_display = self.getMidiRigDisplayAddress()
	    print "address: {}".format(self.midirig_display)
	    self.midirig = self.getMidiRigAddress()
	    if self.midirig:
	    	self.alsaseq.connect_ports(self.midirig_display,self.midirig)
	    	print "Connection successful"
	    	return True
	    else:
		print "MidiRig  not connected"
		return False
	except SequencerError as e:
	    print "Could connect. {}".format(e.message)
	    return False

    def stop(self):
	    self.stop_event.set()

 
    def printConnections(self):	
	conlist = self.alsaseq.connection_list()
	for c in conlist:
	   print "{}, ".format(c[0]),
	   for p in c[2]:
	      print "{}, ".format(p[0]),
	      for cl in p[2]:
		print "\t{}".format(cl)
		

#  "connection_list() -> list\n"
#  "\n"
#  "List all clients and their ports connections.\n"
#  "\n"
#  "Returns:\n"
#  "  (list) a list of tuples: client_name, client_id, port_list:.\n"
#  "    client_name -- the client's name.\n"
#  "    client_id -- the client's id.\n"
#  "    port_list -- a list of tuples: port_name, port_id, connection_list:\n"
#  "      port_name -- the name of the port.\n"
#  "      port_id -- the port id.\n"
#  "      connection_list -- a list of tuples: read_conn, write_conn:\n"
#  "        read_conn -- a list of (client_id, port_id, info) tuples this\n"
#  "                     port is connected to (sends events);\n"
#  "                     info is the same of the get_connect_info() method.\n"
#  "        write_conn -- a list of (client_id, port_id, info) tuples this\n"
#  "                      port is connected from (receives events);\n"
#  "                      info is the same of the get_connect_info() method.\n"
#);
