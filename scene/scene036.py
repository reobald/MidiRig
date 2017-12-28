from mididings import *
from customunits import ProgramChange


def config():
    return Scene("Neo Soul",
                 Pass(),
                 [
                     ProgramChange(1, "STUDIO SET", 36),
                     ProgramChange(16, "NORD ELECTRO", 1)
                 ]
                 )
