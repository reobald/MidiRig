from mididings import *
from customunits import ProgramChange

def config():
	return Scene("Vargar",
                Pass(),
		[
		   ProgramChange(1,"STUDIO SET",8),
		   ProgramChange(16,"NORD ELECTRO",1)		
		]
            )

