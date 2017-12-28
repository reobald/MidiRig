from mididings import *
from customunits import ProgramChange


def config():
    return Scene("Higher ground",
                 Pass(),
                 [
                     ProgramChange(1, "STUDIO SET", 45),
                     ProgramChange(16, "NORD ELECTRO", 6)
                 ]
                 )
