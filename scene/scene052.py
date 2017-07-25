from mididings import *
from customunits import ProgramChange

def config():
	return Scene("Cant take My Eyes Off You",
                Pass(),
		[
		   ProgramChange(1,"STUDIO SET",52),
		   ProgramChange(16,"NORD ELECTRO",1)		
		]
            )

