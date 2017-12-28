from mididings import *
from customunits import ProgramChange


def config():
    return Scene("Play That Funky Music",
                 Pass(),
                 [
                     ProgramChange(1, "STUDIO SET", 24),
                     ProgramChange(16, "NORD ELECTRO", 6)
                 ]
                 )
