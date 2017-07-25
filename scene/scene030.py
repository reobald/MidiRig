from mididings import *
from customunits import ProgramChange

def config():
	return Scene("What a Fool Believes",
                Pass(),
		[
		   ProgramChange(1,"STUDIO SET",30),
		   ProgramChange(16,"NORD ELECTRO",1)		
		]
            )

