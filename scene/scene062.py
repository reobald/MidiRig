from mididings import *
from customunits import ProgramChange

def config():
	return Scene("Let the good times roll",
                Pass(),
		[
		   ProgramChange(16,"NORD ELECTRO",5)		
		]
            )

