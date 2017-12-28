from mididings import *
from customunits import ProgramChange


def config():
    return Scene("I can't stop loving you",
                 Pass(),
                 [
                     ProgramChange(1, "STUDIO SET", 26),
                     ProgramChange(2, "PCMS PRST", 11),
                     ProgramChange(16, "NORD ELECTRO", 1)
                 ]
                 )
