from mididings import *
from customunits import ProgramChange,ConnectSusPedals

def config():
	return Scene("You Can't Hide Love",
                ConnectSusPedals(2,1),
		[
		   ProgramChange(1,"STUDIO SET",55),
		   ProgramChange(16,"NORD ELECTRO",1)		
		]
            )

