from mididings import *
from mididings.extra.gm import *
from customunits import *

def config():
        return Scene("Default",
                Pass(),
		[
		   ProgramChange(1, 'STUDIO SET', 18), 
		   ProgramChange(16,'NORD ELECTRO',1)
		]		
            )

