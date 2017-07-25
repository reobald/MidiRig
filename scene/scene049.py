from mididings import *
from customunits import ProgramChange

def config():
	return Scene("Ain't Nobody",
                ChannelFilter(2)%CtrlMap(11,74),
		[
		   ProgramChange(1,"STUDIO SET",49),
		   ProgramChange(16,"NORD ELECTRO",1)		
		]
            )

