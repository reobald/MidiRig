
from mididings import *
from customunits import ProgramChange
from roland_sysex import Integra7Sysex
from customunits import ProgramChange,ConnectSusPedals

def config():
	name = "Appaloosa"
	integra7sysex = Integra7Sysex()

	nameChange = integra7sysex.generateNameMsg(name)

	part = 3
	channel = 1
	part3ChannelChange = integra7sysex.generateChannelChangeMsg(part,channel)

	part = 2
	volume = 118
	part2VolumeChange = integra7sysex.generateVolumeChangeMsg(part, volume)

	return Scene(name,
		ConnectSusPedals(2,1) >> ChannelFilter(2) % KeySplit('a4',Channel(2),Channel(16)),
#               Pass(),
		[
		   ProgramChange(1,"STUDIO SET",64),
		   ProgramChange(2,"SN-A PRST",1),
		   ProgramChange(1,"PCMS SRX10",4),
		   ProgramChange(3,"SN-S PRST",269),
		   SysEx(nameChange),
		   SysEx(part2VolumeChange),
		   SysEx(part3ChannelChange),
		   ProgramChange(16,"NORD ELECTRO",1)
		]
            )

