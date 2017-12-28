from mididings import *
from customunits import ProgramChange


def config():
    return Scene("Good riddance",
                 Pass(),
                 [
                     ProgramChange(1, "STUDIO SET", 3),
                     ProgramChange(16, "NORD ELECTRO", 1)
                 ]
                 )
