from mididings import *
from mididings.extra import *
from customunits import ProgramChange


def config():
    return Scene("Closer",
                 Pass(),
                 [
                     ProgramChange(1, "STUDIO SET", 13),
                     ProgramChange(16, "NORD ELECTRO", 1)
                 ]
                 )
