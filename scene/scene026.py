from mididings import *
from customunits import ProgramChange

def config():
	return Scene("Brass Octave",
                Pass(),
		[
		   ProgramChange(1,"STUDIO SET",26),
		   ProgramChange(16,"NORD ELECTRO",1)		
		]
            )

