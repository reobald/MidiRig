from mididings import *
from customunits import ProgramChange

def config():
	return Scene("I'm Every Woman",
                Pass(),
		[
		   ProgramChange(1,"STUDIO SET",48),
		   ProgramChange(16,"NORD ELECTRO",1)		
		]
            )

