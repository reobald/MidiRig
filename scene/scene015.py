
from mididings import *
from customunits import ProgramChange
from roland_sysex import Integra7Sysex


def config():
    name = "U shld B dancing"
    integra7sysex = Integra7Sysex()
    msg = integra7sysex.generateNameMsg(name)
    return Scene("You should be dancing",
                 Pass(),
                 [
                     ProgramChange(1, "STUDIO SET", 64),
                     ProgramChange(2, "SN-A USER", 10),
                     ProgramChange(3, "PCMS PRST", 612),
                     ProgramChange(1, "SN-A PRST", 206),
                     SysEx(msg),
                     ProgramChange(16, "NORD ELECTRO", 1)
                 ]
                 )
