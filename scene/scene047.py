from mididings import *
from customunits import ProgramChange


def config():
    return Scene("Watcha Gonna Do",
                 Pass(),
                 [
                     ProgramChange(1, "STUDIO SET", 47),
                     ProgramChange(16, "NORD ELECTRO", 1)
                 ]
                 )
