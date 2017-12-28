from mididings import *
from customunits import ProgramChange


def config():
    return Scene("Land Of Confusion",
                 Pass(),
                 [
                     ProgramChange(1, "STUDIO SET", 53),
                     ProgramChange(16, "NORD ELECTRO", 1)
                 ]
                 )
