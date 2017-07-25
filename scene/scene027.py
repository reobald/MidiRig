from mididings import *
from customunits import ProgramChange

def config():
	return Scene("Everybody wants to rule the world",
                Pass(),
		[
		   ProgramChange(1,"STUDIO SET",27),
		   ProgramChange(16,"NORD ELECTRO",1)		
		]
            )

