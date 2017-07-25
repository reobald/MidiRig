from mididings import *
from customunits import ProgramChange

def config():
	return Scene("Default",
                Pass(),
		[
		   ProgramChange(1,"STUDIO SET",25),
		   ProgramChange(16,"NORD ELECTRO",1)		
		]
            )

