from mididings import *
from customunits import ProgramChange

def config():
	return Scene("Make It Right",
                Pass(),
		[
		   ProgramChange(1,"STUDIO SET",43),
		   ProgramChange(16,"NORD ELECTRO",1)		
		]
            )

