from mididings import *
from customunits import ProgramChange


def config():
    return Scene("Precis som forr",
                 Pass(),
                 [
                     ProgramChange(1, "STUDIO SET", 10),
                     ProgramChange(16, "NORD ELECTRO", 1)
                 ]
                 )
