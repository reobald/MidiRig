from mididings import *
from customunits import ProgramChange

def config():
	return Scene("Africa",
                Pass(),
		[
		   ProgramChange(1,"STUDIO SET",4),
		   ProgramChange(16,"NORD ELECTRO",1)		
		]
            )

