from mididings import *
from customunits import ProgramChange

def config():
	return Scene("Baby Love",
                Pass(),
		[
		   ProgramChange(1,"STUDIO SET",31),
		   ProgramChange(16,"NORD ELECTRO",6)		
		]
            )

