from mididings import *
from customunits import ProgramChange


def config():
    return Scene("Got to give it up",
                 Pass(),
                 [
                     ProgramChange(1, "STUDIO SET", 28),
                     ProgramChange(16, "NORD ELECTRO", 1)
                 ]
                 )
