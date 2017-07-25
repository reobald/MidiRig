from mididings import *
from customunits import ProgramChange

def config():
	return Scene("Bara minnen",
                Pass(),
		[
		   ProgramChange(1,"STUDIO SET",6),
		   ProgramChange(16,"NORD ELECTRO",16)		
		]
            )

