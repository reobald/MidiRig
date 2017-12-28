from mididings import *
from customunits import ProgramChange


def config():
    return Scene("Angelina",
                 Pass(),
                 [
                     ProgramChange(1, "STUDIO SET", 9),
                     ProgramChange(16, "NORD ELECTRO", 1)
                 ]
                 )
