from mididings import *
from customunits import ProgramChange,ConvertExpression

def config():
	return Scene("Everywhere",
		Pass(),
		[
		   ProgramChange(1,"STUDIO SET",15),
		   ProgramChange(16,"NORD ELECTRO",1)		
		]
            )

