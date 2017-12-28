from mididings import *
from customunits import ProgramChange


def config():
    return Scene("Beautiful day",
                 Pass(),
                 [
                     ProgramChange(1, "STUDIO SET", 1),
                     ProgramChange(16, "NORD ELECTRO", 1)
                 ]
                 )
