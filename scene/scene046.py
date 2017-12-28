from mididings import *
from customunits import ProgramChange


def config():
    return Scene("Teardrops",
                 Pass(),
                 [
                     ProgramChange(1, "STUDIO SET", 46),
                     ProgramChange(16, "NORD ELECTRO", 1)
                 ]
                 )
