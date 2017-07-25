from mididings import *
from customunits import ProgramChange

def config():
	return Scene("Call Me Al",
                Pass(),
		[
		   ProgramChange(1,"STUDIO SET",44),
		   ProgramChange(16,"NORD ELECTRO",1)		
		]
            )

