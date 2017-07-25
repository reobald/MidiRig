from mididings import *
from customunits import ProgramChange

def config():
	return Scene("I Wish",
                Pass(),
		[
		   ProgramChange(1,"STUDIO SET",28),
		   ProgramChange(16,"NORD ELECTRO",1)		
		]
            )

