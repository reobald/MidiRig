from mididings import *
from customunits import ProgramChange


def config():
    return Scene("Born to Run",
                 Pass(),
                 [
                     ProgramChange(1, "STUDIO SET", 20),
                     ProgramChange(16, "NORD ELECTRO", 1)
                 ]
                 )
