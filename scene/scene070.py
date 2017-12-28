
from mididings import *
from customunits import ProgramChange
from roland_sysex import Integra7Sysex


def config():
    name = "As"
    integra7sysex = Integra7Sysex()
    msg = integra7sysex.generateNameMsg(name)
    return Scene(name,
                 Pass(),
                 [
                     ProgramChange(1, "STUDIO SET", 64),
                     ProgramChange(2, "SN-A PRST", 14),
                     ProgramChange(1, "SN-S PRST", 977),
                     SysEx(msg),
                     ProgramChange(16, "NORD ELECTRO", 1)
                 ]
                 )
