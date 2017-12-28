from mididings import *
from customunits import ProgramChange


def config():
    return Scene("Use Me",
                 Pass(),
                 [
                     ProgramChange(1, "STUDIO SET", 32),
                     ProgramChange(16, "NORD ELECTRO", 6)
                 ]
                 )
