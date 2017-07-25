
from mididings import *
from customunits import ProgramChange
from roland_sysex import Integra7Sysex

def config():
	name = "On my own"
	integra7sysex = Integra7Sysex()
	msg = integra7sysex.generateNameMsg(name)
	return Scene(name,
                Pass(),
		[
		   ProgramChange(1,"STUDIO SET",64),
		   ProgramChange(16,"NORD ELECTRO",12),
		   ProgramChange(1,"SN-S PRST",425),
		   SysEx(msg)
		]
            )

