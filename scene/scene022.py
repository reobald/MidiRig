from mididings import *
from customunits import ProgramChange


def config():
	return Scene("Billie Jean",
                CtrlFilter(82)%SceneSwitch(number=44),
		[
		   ProgramChange(1,"STUDIO SET",22),
		   ProgramChange(16,"NORD ELECTRO",1)		
		]
            )

