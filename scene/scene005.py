from mididings import *
from customunits import ProgramChange, ConvertExpression


def config():
    return Scene(
        "Evelina", (ChannelFilter(4) & CtrlFilter(11)) %
        ConvertExpression(
            4, 74) >> CtrlRange(
            74, 20, 120), [
                ProgramChange(
                    1, "STUDIO SET", 5), ProgramChange(
                        16, "NORD ELECTRO", 1)])
