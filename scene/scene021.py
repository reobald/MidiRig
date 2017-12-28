from mididings import *
from customunits import ProgramChange, ConnectSusPedals


def config():
    return Scene("Human Nature",
                 ConnectSusPedals(2, 1),
                 [
                     ProgramChange(1, "STUDIO SET", 21),
                     ProgramChange(16, "NORD ELECTRO", 1)
                 ]
                 )
