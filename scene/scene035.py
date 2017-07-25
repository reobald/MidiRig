from mididings import *
from customunits import ProgramChange,ConvertExpression

def config():
	return Scene("Boys Of Summer",
                ConvertExpression(2,74)>>CtrlRange(74,60,120),
		[
		   ProgramChange(1,"STUDIO SET",35),
		   ProgramChange(16,"NORD ELECTRO",1)		
		]
            )

