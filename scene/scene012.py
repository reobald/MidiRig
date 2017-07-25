from mididings import *
from customunits import ProgramChange

def config():
	return Scene("Anglars tarar",
                Pass(),
		[
		   ProgramChange(1,"STUDIO SET",12),
		   ProgramChange(16,"NORD ELECTRO",1)		
		]
            )

