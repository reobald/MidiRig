from mididings import *
from customunits import ProgramChange


def config():
    return Scene("Det stora blaa",
                 Pass(),
                 [
                     ProgramChange(1, "STUDIO SET", 7),
                     ProgramChange(16, "NORD ELECTRO", 1)
                 ]
                 )
