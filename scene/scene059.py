
from mididings import *
from customunits import ProgramChange
from arturia_sysex import ArturiaSysex

def config():
	name = "Arturiatest"
	arturiasysex = ArturiaSysex()
	msg = arturiasysex.generateNameMsg(name)
	return Scene(name,
                Pass(),
		[
		   ProgramChange(1,"STUDIO SET",64),
		   ProgramChange(2,"SN-A PRST",14),
		   ProgramChange(1,"SN-S PRST",977),
		   SysEx(msg),
		   ProgramChange(16,"NORD ELECTRO",1)
		]
            )

