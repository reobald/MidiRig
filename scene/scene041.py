from mididings import *
from customunits import ProgramChange

def config():
	return Scene("I Can't Go For That",
                Pass(),
		[
		   ProgramChange(1,"STUDIO SET",41),
		   ProgramChange(16,"NORD ELECTRO",1)		
		]
            )

