from mididings import *
from customunits import ProgramChange


def config():
    return Scene("Ain't that peculiar",
                 Pass(),
                 [
                     ProgramChange(1, "STUDIO SET", 26),
                     ProgramChange(16, "NORD ELECTRO", 6)
                 ]
                 )
