from mididings import *
from customunits import ProgramChange

def config():
	return Scene("SledgeHammer",
                Pass(),
		[
		   ProgramChange(1,"STUDIO SET",19),
		   ProgramChange(16,"NORD ELECTRO",1)		
		]
            )

