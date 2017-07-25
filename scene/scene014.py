from mididings import *
from mididings.extra import *
from customunits import ProgramChange

def config():
	return Scene("Timberlake",
               CtrlRange(11,127,80)>>CtrlFilter(11)%[Pass(),Channel(1)],
		[
		   ProgramChange(1,'STUDIO SET', 14), 
		   ProgramChange(16, 'NORD ELECTRO', 1),
		]
            )

