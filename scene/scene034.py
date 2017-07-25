from mididings import *
from customunits import ProgramChange

def config():
	return Scene("Do I Do",
                Pass(),
		[
		   ProgramChange(1,"STUDIO SET",34),
		   ProgramChange(16,"NORD ELECTRO",1)		
		]
            )

