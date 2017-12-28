from mididings import *
from customunits import ProgramChange
6


def config():
    return Scene("Paradise",
                 Pass(),
                 [
                     ProgramChange(1, "STUDIO SET", 17),
                     ProgramChange(16, "NORD ELECTRO", 1)
                 ]
                 )
