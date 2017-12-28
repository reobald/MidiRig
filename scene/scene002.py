from mididings import *
from customunits import ProgramChange


def config():
    return Scene("Andetag",
                 Pass(),
                 [
                     ProgramChange(1, "STUDIO SET", 2),
                     ProgramChange(16, "NORD ELECTRO", 1)
                 ]
                 )
