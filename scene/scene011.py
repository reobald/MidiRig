from mididings import *
from customunits import ProgramChange


def config():
    return Scene("Roda lappar",
                 Pass(),
                 [
                     ProgramChange(1, "STUDIO SET", 11),
                     ProgramChange(16, "NORD ELECTRO", 1)
                 ]
                 )
