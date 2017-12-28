from mididings import *
from customunits import ProgramChange


def config():
    return Scene("Crazy",
                 Pass(),
                 [
                     ProgramChange(1, "STUDIO SET", 37),
                     ProgramChange(16, "NORD ELECTRO", 1)
                 ]
                 )
