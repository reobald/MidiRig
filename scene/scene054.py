from mididings import *
from customunits import ProgramChange


def config():
    return Scene("Pick Up The Pieces",
                 Pass(),
                 [
                     ProgramChange(1, "STUDIO SET", 54),
                     ProgramChange(16, "NORD ELECTRO", 1)
                 ]
                 )
