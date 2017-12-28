from mididings import *
from customunits import ProgramChange


def config():
    return Scene("I Keep Forgetting",
                 Pass(),
                 [
                     ProgramChange(1, "STUDIO SET", 39),
                     ProgramChange(16, "NORD ELECTRO", 1)
                 ]
                 )
