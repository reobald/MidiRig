from mididings import *
from customunits import ProgramChange

def config():
	return Scene("Sharp Dressed Man",
                Pass(),
		[
		   ProgramChange(1,"STUDIO SET",33),
		   ProgramChange(16,"NORD ELECTRO",1)		
		]
            )

