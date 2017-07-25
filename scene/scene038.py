from mididings import *
from customunits import ProgramChange

def config():
	return Scene("Happy",
                Pass(),
		[
		   ProgramChange(1,"STUDIO SET",38),
		   ProgramChange(16,"NORD ELECTRO",3)		
		]
            )

