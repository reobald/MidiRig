from mididings import *
from customunits import ProgramChange


ifExprOnMidiCh2 = (ChannelFilter(2) & CtrlFilter(11))
ifChannel2 = ChannelFilter(2)


def config():
    return Scene(
        "In the Air Tonight", ifExprOnMidiCh2 %
        (Channel(3) >> CtrlMap(
            11, 74) >> CtrlRange(
            74, 40, 127)) >> ifChannel2 %
        [
            Pass(), Channel(3)], [
            ProgramChange(
                1, "STUDIO SET", 51), ProgramChange(
                16, "NORD ELECTRO", 1)])
