from mididings import *
from customunits import ProgramChange

def config():
	return Scene("Driven to Tears",
                Pass(),
		[
		   ProgramChange(1,"STUDIO SET",40),
		   ProgramChange(16,"NORD ELECTRO",1)		
		]
            )

