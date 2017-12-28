from mididings import *
from customunits import ProgramChange, ConvertExpression


def config():
    return Scene("Some die young",
                 Pass(),
                 [
                     ProgramChange(1, "STUDIO SET", 52),
                     ProgramChange(16, "NORD ELECTRO", 1)
                 ]
                 )
