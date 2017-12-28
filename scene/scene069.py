from mididings import *
from customunits import ProgramChange


def config():
    return Scene("Like wine",
                 Pass(),
                 [
                     ProgramChange(16, "NORD ELECTRO", 9)
                 ]
                 )
