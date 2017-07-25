from mididings import *
from customunits import ProgramChange

def config():
	return Scene("Could You Be Loved",
                Pass(),
		[
		   ProgramChange(1,"STUDIO SET",29),
		   ProgramChange(16,"NORD ELECTRO",4)		
		]
            )

