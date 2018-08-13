from mididings import *
from customunits import ProgramChange,ConvertExpression, ConnectSusPedals
from mididings.extra import *
from roland_sysex import Integra7Sysex
from mididings.event import MidiEvent
from africa_solo import ResetAfricaSolo, HarmonizeAfricaSolo
import arturia_sysex
from constants import DEFAULT_PORT

def initUpperKeybController(channel_mapping,scene,channel):
    channel_mapping.add_upper_keyb_init(scene, channel)
    if 15 <= channel <= 16:
        btn_nr = channel-6
    else:
        btn_nr = (channel-1)&7
    return arturia_sysex.generateToggledButtonPatches(btn_nr)

def initLowerKeybController(channel_mapping,scene,channel):
    channel_mapping.add_lower_keyb_init(scene, channel)
    if 15 <= channel <= 16:
        pgm_nr = channel-8
    else:
        pgm_nr = ((channel-1)&7)+1
    pgm_ch = channel_mapping.lower_source_ch
    return Program(DEFAULT_PORT, pgm_ch, pgm_nr)

def default(channel_mapping,scene):
    UpperKeybInit = initUpperKeybController(channel_mapping,scene, 1)
    LowerKeybInit = initLowerKeybController(channel_mapping,scene, 2)
    return Scene("Default",
                Pass(),
                [
                    ProgramChange(1, "STUDIO SET", 18),
                    ProgramChange(16, "NORD ELECTRO", 1),
                    UpperKeybInit,
                    LowerKeybInit
                ]
                )


def beautiful_day(channel_mapping,scene):
    UpperKeybInit = initUpperKeybController(channel_mapping,scene, 1)
    LowerKeybInit = initLowerKeybController(channel_mapping,scene, 2)
    return Scene("Beautiful day",
                 Pass(),
                 [
                     ProgramChange(1, "STUDIO SET", 1),
                     ProgramChange(16, "NORD ELECTRO", 1),
                     UpperKeybInit,
                     LowerKeybInit
                 ]
                 )


def andetag(channel_mapping,scene):
    UpperKeybInit = initUpperKeybController(channel_mapping,scene, 1)
    LowerKeybInit = initLowerKeybController(channel_mapping,scene, 2)
    return Scene("Andetag",
                 Pass(),
                 [
                     ProgramChange(1, "STUDIO SET", 2),
                     ProgramChange(16, "NORD ELECTRO", 25),
                     UpperKeybInit,
                     LowerKeybInit
                 ]
                 )


def _24_k_magic(channel_mapping,scene):
    UpperKeybInit = initUpperKeybController(channel_mapping,scene, 1)
    LowerKeybInit = initLowerKeybController(channel_mapping,scene, 2)
    return Scene("24K Magic",
                 Pass(),
                 [
                     ProgramChange(1, "STUDIO SET", 36),
                     ProgramChange(16, "NORD ELECTRO", 1),
                     UpperKeybInit,
                     LowerKeybInit
                 ]
                 )

def africa(channel_mapping,scene):
    UpperKeybInit = initUpperKeybController(channel_mapping,scene, 1)
    LowerKeybInit = initLowerKeybController(channel_mapping,scene, 2)
    return Scene("Africa",
                (ChannelFilter(4) % HarmonizeAfricaSolo()),
                 [
                     ResetAfricaSolo(),
                     ProgramChange(1, "STUDIO SET", 4),
                     ProgramChange(16, "NORD ELECTRO", 1),
                     UpperKeybInit,
                     LowerKeybInit
                 ]
                ) 


def evelina(channel_mapping,scene):
    UpperKeybInit = initUpperKeybController(channel_mapping,scene, 3)
    LowerKeybInit = initLowerKeybController(channel_mapping,scene, 16)
    return Scene("Evelina",
                 ConnectSusPedals(3,2), 
                 [
                     ProgramChange(1, "STUDIO SET", 5), 
                     ProgramChange(16, "NORD ELECTRO", 1),
                     UpperKeybInit,
                     LowerKeybInit
                 ]
                )


def bara_minnen(channel_mapping,scene):
    UpperKeybInit = initUpperKeybController(channel_mapping,scene, 1)
    LowerKeybInit = initLowerKeybController(channel_mapping,scene, 16)
    return Scene("Bara minnen",
                 Pass(),
                 [
                     ProgramChange(1, "STUDIO SET", 6),
                     ProgramChange(16, "NORD ELECTRO", 16),
                     UpperKeybInit,
                     LowerKeybInit
                 ]
                 )


def det_stora_blaa(channel_mapping,scene):
    UpperKeybInit = initUpperKeybController(channel_mapping,scene, 1)
    LowerKeybInit = initLowerKeybController(channel_mapping,scene, 16)
    return Scene("Det stora blaa",
                 Pass(),
                 [
                     ProgramChange(1, "STUDIO SET", 7),
                     ProgramChange(16, "NORD ELECTRO", 1),
                     UpperKeybInit,
                     LowerKeybInit
                 ]
                 )


def vargar(channel_mapping,scene):
    UpperKeybInit = initUpperKeybController(channel_mapping,scene, 1)
    LowerKeybInit = initLowerKeybController(channel_mapping,scene, 16)
    return Scene("Vargar",
                 Pass(),
                 [
                     ProgramChange(1, "STUDIO SET", 8),
                     ProgramChange(16, "NORD ELECTRO", 1),
                     UpperKeybInit,
                     LowerKeybInit
                 ]
                 )


def angelina(channel_mapping,scene):
    UpperKeybInit = initUpperKeybController(channel_mapping,scene, 1)
    LowerKeybInit = initLowerKeybController(channel_mapping,scene, 16)
    return Scene("Angelina",
                 Pass(),
                 [
                     ProgramChange(1, "STUDIO SET", 9),
                     ProgramChange(16, "NORD ELECTRO", 1),
                     UpperKeybInit,
                     LowerKeybInit
                 ]
                 )


def precis_som_forr(channel_mapping,scene):
    UpperKeybInit = initUpperKeybController(channel_mapping,scene, 1)
    LowerKeybInit = initLowerKeybController(channel_mapping,scene, 2)
    return Scene("Precis som forr",
                 Pass(),
                 [
                     ProgramChange(1, "STUDIO SET", 10),
                     ProgramChange(16, "NORD ELECTRO", 1),
                     UpperKeybInit,
                     LowerKeybInit
                 ]
                 )


def roda_lappar(channel_mapping,scene):
    UpperKeybInit = initUpperKeybController(channel_mapping,scene, 1)
    LowerKeybInit = initLowerKeybController(channel_mapping,scene, 16)
    return Scene("Roda lappar",
                 Pass(),
                 [
                     ProgramChange(1, "STUDIO SET", 11),
                     ProgramChange(16, "NORD ELECTRO", 1),
                     UpperKeybInit,
                     LowerKeybInit
                 ]
                 )


def anglars_tarar(channel_mapping,scene):
    UpperKeybInit = initUpperKeybController(channel_mapping,scene, 1)
    LowerKeybInit = initLowerKeybController(channel_mapping,scene, 16)
    return Scene("Anglars tarar",
                 Pass(),
                 [
                     ProgramChange(1, "STUDIO SET", 12),
                     ProgramChange(16, "NORD ELECTRO", 1),
                     UpperKeybInit,
                     LowerKeybInit
                 ]
                 )


def closer(channel_mapping,scene):
    UpperKeybInit = initUpperKeybController(channel_mapping,scene, 1)
    LowerKeybInit = initLowerKeybController(channel_mapping,scene, 2)
    return Scene("Closer",
                 Pass(),
                 [
                     ProgramChange(1, "STUDIO SET", 13),
                     ProgramChange(16, "NORD ELECTRO", 1),
                     UpperKeybInit,
                     LowerKeybInit
                 ]
                 )


def timberlake(channel_mapping,scene):
    UpperKeybInit = initUpperKeybController(channel_mapping,scene, 1)
    LowerKeybInit = initLowerKeybController(channel_mapping,scene, 2)
    return Scene("Timberlake",
                 CtrlRange(11, 127, 80) >> CtrlFilter(
                     11) % [Pass(), Channel(1)],
                 [
                     ProgramChange(1, 'STUDIO SET', 14),
                     ProgramChange(16, 'NORD ELECTRO', 1),
                     UpperKeybInit,
                     LowerKeybInit
                 ]
                 )


def you_should_be_dancing(channel_mapping,scene):
    name = "U shld B dancing"
    integra7sysex = Integra7Sysex()
    msg = integra7sysex.generateNameMsg(name)
    UpperKeybInit = initUpperKeybController(channel_mapping,scene, 1)
    LowerKeybInit = initLowerKeybController(channel_mapping,scene, 2)
    return Scene("You should be dancing",
                 Pass(),
                 [
                     ProgramChange(1, "STUDIO SET", 64),
                     ProgramChange(2, "SN-A USER", 10),
                     ProgramChange(3, "PCMS PRST", 612),
                     ProgramChange(1, "SN-A PRST", 206),
                     SysEx(msg),
                     ProgramChange(16, "NORD ELECTRO", 1),
                     UpperKeybInit,
                     LowerKeybInit
                 ]
                 )


def on_my_own(channel_mapping,scene):
    name = "On my own"
    integra7sysex = Integra7Sysex()
    msg = integra7sysex.generateNameMsg(name)
    UpperKeybInit = initUpperKeybController(channel_mapping,scene, 1)
    LowerKeybInit = initLowerKeybController(channel_mapping,scene, 2)
    return Scene(name,
                 Pass(),
                 [
                     ProgramChange(1, "STUDIO SET", 64),
                     ProgramChange(16, "NORD ELECTRO", 12),
                     ProgramChange(1, "SN-S PRST", 425),
                     SysEx(msg),
                     UpperKeybInit,
                     LowerKeybInit
                 ]
                 )


def paradise(channel_mapping,scene):
    UpperKeybInit = initUpperKeybController(channel_mapping,scene, 1)
    LowerKeybInit = initLowerKeybController(channel_mapping,scene, 2)
    return Scene("Paradise",
                 Pass(),
                 [
                     ProgramChange(1, "STUDIO SET", 17),
                     ProgramChange(16, "NORD ELECTRO", 1),
                     UpperKeybInit,
                     LowerKeybInit
                 ]
                 )


def beautiful_day(channel_mapping,scene):
    UpperKeybInit = initUpperKeybController(channel_mapping,scene, 1)
    LowerKeybInit = initLowerKeybController(channel_mapping,scene, 2)
    return Scene("Beautiful day",
                 Pass(),
                 [
                     ProgramChange(1, "STUDIO SET", 1),
                     ProgramChange(16, "NORD ELECTRO", 1),
                     UpperKeybInit,
                     LowerKeybInit
                 ]
                 )


def sledgehammer(channel_mapping,scene):
    UpperKeybInit = initUpperKeybController(channel_mapping,scene, 16)
    LowerKeybInit = initLowerKeybController(channel_mapping,scene, 2)
    return Scene("SledgeHammer",
                 Pass(),
                 [
                     ProgramChange(1, "STUDIO SET", 19),
                     ProgramChange(16, "NORD ELECTRO", 1),
                     UpperKeybInit,
                     LowerKeybInit
                 ]
                 )


def born_to_run(channel_mapping,scene):
    UpperKeybInit = initUpperKeybController(channel_mapping,scene, 1)
    LowerKeybInit = initLowerKeybController(channel_mapping,scene, 2)
    return Scene("Born to Run",
                 Pass(),
                 [
                     ProgramChange(1, "STUDIO SET", 20),
                     ProgramChange(16, "NORD ELECTRO", 1),
                     UpperKeybInit,
                     LowerKeybInit
                 ]
                 )


def human_nature(channel_mapping,scene):
    UpperKeybInit = initUpperKeybController(channel_mapping,scene, 1)
    LowerKeybInit = initLowerKeybController(channel_mapping,scene, 2)
    return Scene("Human Nature",
                 ConnectSusPedals(2, 1),
                 [
                     ProgramChange(1, "STUDIO SET", 21),
                     ProgramChange(16, "NORD ELECTRO", 1),
                     UpperKeybInit,
                     LowerKeybInit
                 ]
                 )


def billie_jean(channel_mapping,scene):
    UpperKeybInit = initUpperKeybController(channel_mapping,scene, 1)
    LowerKeybInit = initLowerKeybController(channel_mapping,scene, 2)
    return Scene("Billie Jean",
                 CtrlFilter(82) % SceneSwitch(number=45),
                 [
                     ProgramChange(1, "STUDIO SET", 22),
                     ProgramChange(16, "NORD ELECTRO", 1),
                     UpperKeybInit,
                     LowerKeybInit
                 ]
                 )


def staying_alive(channel_mapping,scene):
    name = "Staying alive"
    integra7sysex = Integra7Sysex()
    msg = integra7sysex.generateNameMsg(name)
    UpperKeybInit = initUpperKeybController(channel_mapping,scene, 1)
    LowerKeybInit = initLowerKeybController(channel_mapping,scene, 2)
    return Scene(name,
                 Pass(),
                 [
                     ProgramChange(1, "STUDIO SET", 64),
                     ProgramChange(2, "SN-A PRST", 10),
                     ProgramChange(1, "SN-A PRST", 208),
                     SysEx(msg),
                     ProgramChange(16, "NORD ELECTRO", 1),
                     UpperKeybInit,
                     LowerKeybInit
                 ]
                 )


def play_that_funky_music(channel_mapping,scene):
    UpperKeybInit = initUpperKeybController(channel_mapping,scene, 1)
    LowerKeybInit = initLowerKeybController(channel_mapping,scene, 16)
    return Scene("Play That Funky Music",
                 Pass(),
                 [
                     ProgramChange(1, "STUDIO SET", 24),
                     ProgramChange(16, "NORD ELECTRO", 6),
                     UpperKeybInit,
                     LowerKeybInit
                 ]
                 )


def brass_octave(channel_mapping,scene):
    UpperKeybInit = initUpperKeybController(channel_mapping,scene, 1)
    LowerKeybInit = initLowerKeybController(channel_mapping,scene, 2)
    return Scene("Brass Octave",
                 Pass(),
                 [
                     ProgramChange(1, "STUDIO SET", 26),
                     ProgramChange(16, "NORD ELECTRO", 1),
                     UpperKeybInit,
                     LowerKeybInit
                 ]
                 )


def everybody_wants_to_rule_the_world(channel_mapping,scene):
    UpperKeybInit = initUpperKeybController(channel_mapping,scene, 1)
    LowerKeybInit = initLowerKeybController(channel_mapping,scene, 2)
    return Scene("Everybody wants to rule the world",
                 Pass(),
                 [
                     ProgramChange(1, "STUDIO SET", 27),
                     ProgramChange(16, "NORD ELECTRO", 1),
                     UpperKeybInit,
                     LowerKeybInit
                 ]
                 )


def i_wish(channel_mapping,scene):
    UpperKeybInit = initUpperKeybController(channel_mapping,scene, 1)
    LowerKeybInit = initLowerKeybController(channel_mapping,scene, 2)
    return Scene("I Wish",
                 Pass(),
                 [
                     ProgramChange(1, "STUDIO SET", 28),
                     ProgramChange(16, "NORD ELECTRO", 1),
                     UpperKeybInit,
                     LowerKeybInit
                 ]
                 )


def could_you_be_loved(channel_mapping,scene):
    UpperKeybInit = initUpperKeybController(channel_mapping,scene, 1)
    LowerKeybInit = initLowerKeybController(channel_mapping,scene, 16)
    return Scene("Could You Be Loved",
                 Pass(),
                 [
                     ProgramChange(1, "STUDIO SET", 29),
                     ProgramChange(16, "NORD ELECTRO", 4),
                     UpperKeybInit,
                     LowerKeybInit
                 ]
                 )


def what_a_fool_believes(channel_mapping,scene):
    UpperKeybInit = initUpperKeybController(channel_mapping,scene, 1)
    LowerKeybInit = initLowerKeybController(channel_mapping,scene, 2)
    return Scene("What a Fool Believes",
                 Pass(),
                 [
                     ProgramChange(1, "STUDIO SET", 30),
                     ProgramChange(16, "NORD ELECTRO", 1),
                     UpperKeybInit,
                     LowerKeybInit
                 ]
                 )


def baby_love(channel_mapping,scene):
    UpperKeybInit = initUpperKeybController(channel_mapping,scene, 1)
    LowerKeybInit = initLowerKeybController(channel_mapping,scene, 16)
    return Scene("Baby Love",
                 Pass(),
                 [
                     ProgramChange(1, "STUDIO SET", 31),
                     ProgramChange(16, "NORD ELECTRO", 6),
                     UpperKeybInit,
                     LowerKeybInit
                 ]
                 )


def use_me(channel_mapping,scene):
    UpperKeybInit = initUpperKeybController(channel_mapping,scene, 1)
    LowerKeybInit = initLowerKeybController(channel_mapping,scene, 16)
    return Scene("Use Me",
                 Pass(),
                 [
                     ProgramChange(1, "STUDIO SET", 32),
                     ProgramChange(16, "NORD ELECTRO", 6),
                     UpperKeybInit,
                     LowerKeybInit
                 ]
                 )


def sharp_dressed_man(channel_mapping,scene):
    UpperKeybInit = initUpperKeybController(channel_mapping,scene, 1)
    LowerKeybInit = initLowerKeybController(channel_mapping,scene, 16)
    return Scene("Sharp Dressed Man",
                 Pass(),
                 [
                     ProgramChange(1, "STUDIO SET", 33),
                     ProgramChange(16, "NORD ELECTRO", 1),
                     UpperKeybInit,
                     LowerKeybInit
                 ]
                 )


def do_i_do(channel_mapping,scene):
    UpperKeybInit = initUpperKeybController(channel_mapping,scene, 1)
    LowerKeybInit = initLowerKeybController(channel_mapping,scene, 3)
    return Scene("Do I Do",
                 Pass(),
                 [
                     ProgramChange(1, "STUDIO SET", 34),
                     ProgramChange(16, "NORD ELECTRO", 1),
                     UpperKeybInit,
                     LowerKeybInit
                 ]
                 )


def boys_of_summer(channel_mapping,scene):
    UpperKeybInit = initUpperKeybController(channel_mapping,scene, 1)
    LowerKeybInit = initLowerKeybController(channel_mapping,scene, 2)
    return Scene("Boys Of Summer",
                 ConvertExpression(2, 74) >> CtrlRange(74, 60, 120),
                 [
                     ProgramChange(1, "STUDIO SET", 35),
                     ProgramChange(16, "NORD ELECTRO", 1),
                     UpperKeybInit,
                     LowerKeybInit
                 ]
                 )


def neo_soul(channel_mapping,scene):
    UpperKeybInit = initUpperKeybController(channel_mapping,scene, 1)
    LowerKeybInit = initLowerKeybController(channel_mapping,scene, 2)
    return Scene("Neo Soul",
                 Pass(),
                 [
                     ProgramChange(1, "STUDIO SET", 36),
                     ProgramChange(16, "NORD ELECTRO", 1),
                     UpperKeybInit,
                     LowerKeybInit
                 ]
                 )


def crazy(channel_mapping,scene):
    UpperKeybInit = initUpperKeybController(channel_mapping,scene, 1)
    LowerKeybInit = initLowerKeybController(channel_mapping,scene, 2)
    return Scene("Crazy",
                 Pass(),
                 [
                     ProgramChange(1, "STUDIO SET", 37),
                     ProgramChange(16, "NORD ELECTRO", 1),
                     UpperKeybInit,
                     LowerKeybInit
                 ]
                 )


def happy(channel_mapping,scene):
    UpperKeybInit = initUpperKeybController(channel_mapping,scene, 1)
    LowerKeybInit = initLowerKeybController(channel_mapping,scene, 16)
    return Scene("Happy",
                 Pass(),
                 [
                     ProgramChange(1, "STUDIO SET", 38),
                     ProgramChange(16, "NORD ELECTRO", 3),
                     UpperKeybInit,
                     LowerKeybInit
                 ]
                 )


def i_keep_forgetting(channel_mapping,scene):
    UpperKeybInit = initUpperKeybController(channel_mapping,scene, 1)
    LowerKeybInit = initLowerKeybController(channel_mapping,scene, 2)
    return Scene("I Keep Forgetting",
                 Pass(),
                 [
                     ProgramChange(1, "STUDIO SET", 39),
                     ProgramChange(16, "NORD ELECTRO", 1),
                     UpperKeybInit,
                     LowerKeybInit
                 ]
                 )


def driven_to_tears(channel_mapping,scene):
    UpperKeybInit = initUpperKeybController(channel_mapping,scene, 1)
    LowerKeybInit = initLowerKeybController(channel_mapping,scene, 16)
    return Scene("Driven to Tears",
                 Pass(),
                 [
                     ProgramChange(1, "STUDIO SET", 40),
                     ProgramChange(16, "NORD ELECTRO", 1),
                     UpperKeybInit,
                     LowerKeybInit
                 ]
                 )


def i_cant_go_for_that(channel_mapping,scene):
    UpperKeybInit = initUpperKeybController(channel_mapping,scene, 1)
    LowerKeybInit = initLowerKeybController(channel_mapping,scene, 2)
    return Scene("I Can't Go For That",
                 Pass(),
                 [
                     ProgramChange(1, "STUDIO SET", 41),
                     ProgramChange(16, "NORD ELECTRO", 1),
                     UpperKeybInit,
                     LowerKeybInit
                 ]
                 )


def wurlitzer(channel_mapping,scene):
    name = "Wurlitzer"
    integra7sysex = Integra7Sysex()
    msg = integra7sysex.generateNameMsg(name)
    UpperKeybInit = initUpperKeybController(channel_mapping,scene, 1)
    LowerKeybInit = initLowerKeybController(channel_mapping,scene, 2)
    return Scene(name,
                 Pass(),
                 [
                     ProgramChange(1, "STUDIO SET", 64),
                     ProgramChange(2, "SN-A PRST", 32),
                     SysEx(msg),
                     ProgramChange(16, "NORD ELECTRO", 1),
                     UpperKeybInit,
                     LowerKeybInit
                 ]
                 )


def make_it_right(channel_mapping,scene):
    UpperKeybInit = initUpperKeybController(channel_mapping,scene, 1)
    LowerKeybInit = initLowerKeybController(channel_mapping,scene, 2)
    return Scene("Make It Right",
                 Pass(),
                 [
                     ProgramChange(1, "STUDIO SET", 43),
                     ProgramChange(16, "NORD ELECTRO", 1),
                     UpperKeybInit,
                     LowerKeybInit
                 ]
                 )


def call_me_al(channel_mapping,scene):
    UpperKeybInit = initUpperKeybController(channel_mapping,scene, 1)
    LowerKeybInit = initLowerKeybController(channel_mapping,scene, 2)
    return Scene("Call Me Al",
                 Pass(),
                 [
                     ProgramChange(1, "STUDIO SET", 44),
                     ProgramChange(16, "NORD ELECTRO", 1),
                     UpperKeybInit,
                     LowerKeybInit
                 ]
                 )


def the_way_you_make_me_feel(channel_mapping,scene):
    UpperKeybInit = initUpperKeybController(channel_mapping,scene, 1)
    LowerKeybInit = initLowerKeybController(channel_mapping,scene, 2)
    return Scene("The Way You Make Me Feel",
                 Pass(),
                 [
                     ProgramChange(1, "STUDIO SET", 45),
                     ProgramChange(16, "NORD ELECTRO", 6),
                     UpperKeybInit,
                     LowerKeybInit
                 ]
                 )


def teardrops(channel_mapping,scene):
    UpperKeybInit = initUpperKeybController(channel_mapping,scene, 1)
    LowerKeybInit = initLowerKeybController(channel_mapping,scene, 2)
    return Scene("Teardrops",
                 Pass(),
                 [
                     ProgramChange(1, "STUDIO SET", 46),
                     ProgramChange(16, "NORD ELECTRO", 1),
                     UpperKeybInit,
                     LowerKeybInit
                 ]
                 )


def watcha_gonna_do(channel_mapping,scene):
    UpperKeybInit = initUpperKeybController(channel_mapping,scene, 1)
    LowerKeybInit = initLowerKeybController(channel_mapping,scene, 2)
    return Scene("Watcha Gonna Do",
                 Pass(),
                 [
                     ProgramChange(1, "STUDIO SET", 47),
                     ProgramChange(16, "NORD ELECTRO", 1),
                     UpperKeybInit,
                     LowerKeybInit
                 ]
                 )


def im_every_woman(channel_mapping,scene):
    UpperKeybInit = initUpperKeybController(channel_mapping,scene, 1)
    LowerKeybInit = initLowerKeybController(channel_mapping,scene, 2)
    return Scene("I'm Every Woman",
                 Pass(),
                 [
                     ProgramChange(1, "STUDIO SET", 48),
                     ProgramChange(16, "NORD ELECTRO", 1),
                     UpperKeybInit,
                     LowerKeybInit
                 ]
                 )


def aint_nobody(channel_mapping,scene):
    UpperKeybInit = initUpperKeybController(channel_mapping,scene, 1)
    LowerKeybInit = initLowerKeybController(channel_mapping,scene, 2)
    return Scene("Ain't Nobody",
                 ChannelFilter(2) % CtrlMap(11, 74),
                 [
                     ProgramChange(1, "STUDIO SET", 49),
                     ProgramChange(16, "NORD ELECTRO", 1),
                     UpperKeybInit,
                     LowerKeybInit
                 ]
                 )


def appaloosa(channel_mapping,scene):
    name = "Appaloosa"
    integra7sysex = Integra7Sysex()

    nameChange = integra7sysex.generateNameMsg(name)

    part = 3
    channel = 1
    part3ChannelChange = integra7sysex.generateChannelChangeMsg(part, channel)

    part = 2
    volume = 118
    part2VolumeChange = integra7sysex.generateVolumeChangeMsg(part, volume)

    UpperKeybInit = initUpperKeybController(channel_mapping,scene, 1)
    LowerKeybInit = initLowerKeybController(channel_mapping,scene, 2)
    return Scene(name,
                 ConnectSusPedals(
                     2,
                     1) >> ChannelFilter(2) % KeySplit(
                     'a4',
                     Channel(2),
                     Channel(16)),
                 #               Pass(),
                 [
                     ProgramChange(1, "STUDIO SET", 64),
                     ProgramChange(2, "SN-A PRST", 1),
                     ProgramChange(1, "PCMS SRX10", 4),
                     ProgramChange(3, "SN-S PRST", 269),
                     SysEx(nameChange),
                     SysEx(part2VolumeChange),
                     SysEx(part3ChannelChange),
                     ProgramChange(16, "NORD ELECTRO", 1),
                     UpperKeybInit,
                     LowerKeybInit
                 ]
                 )


def in_the_air_tonight(channel_mapping,scene):
    ifExprOnMidiCh2 = (ChannelFilter(2) & CtrlFilter(11))
    ifChannel2 = ChannelFilter(2)
    UpperKeybInit = initUpperKeybController(channel_mapping,scene, 1)
    LowerKeybInit = initLowerKeybController(channel_mapping,scene, 2)
    return Scene("In the Air Tonight", 
                ifExprOnMidiCh2 % \
                (Channel(3) >> \
                CtrlMap( 11, 74) >> \
                CtrlRange(74, 40, 127)) >> \
                ifChannel2 %
                    [ Pass(), Channel(3)], 
                    [
                        ProgramChange(1, "STUDIO SET", 51), 
                        ProgramChange(16, "NORD ELECTRO", 1),
                     UpperKeybInit,
                     LowerKeybInit
                    ]
                    )


def hard_to_handle(channel_mapping,scene):
    UpperKeybInit = initUpperKeybController(channel_mapping,scene, 1)
    LowerKeybInit = initLowerKeybController(channel_mapping,scene, 2)
    return Scene("Hard to handle",
                 Pass(),
                 [
                     ProgramChange(1, "STUDIO SET", 52),
                     ProgramChange(16, "NORD ELECTRO", 1),
                     UpperKeybInit,
                     LowerKeybInit
                 ]
                 )


def land_of_confusion(channel_mapping,scene):
    UpperKeybInit = initUpperKeybController(channel_mapping,scene, 1)
    LowerKeybInit = initLowerKeybController(channel_mapping,scene, 3)
    return Scene("Land Of Confusion",
                 Pass(),
                 [
                     ProgramChange(1, "STUDIO SET", 53),
                     ProgramChange(16, "NORD ELECTRO", 1),
                     UpperKeybInit,
                     LowerKeybInit
                 ]
                 )


def pick_up_the_pieces(channel_mapping,scene):
    UpperKeybInit = initUpperKeybController(channel_mapping,scene, 16)
    LowerKeybInit = initLowerKeybController(channel_mapping,scene, 15)
    return Scene("Pick Up The Pieces",
                 Pass(),
                 [
                     ProgramChange(1, "STUDIO SET", 54),
                     ProgramChange(16, "NORD ELECTRO", 1),
                     UpperKeybInit,
                     LowerKeybInit
                 ]
                 )


def you_cant_hide_love(channel_mapping,scene):
    UpperKeybInit = initUpperKeybController(channel_mapping,scene, 1)
    LowerKeybInit = initLowerKeybController(channel_mapping,scene, 2)
    return Scene("You Can't Hide Love",
                 ConnectSusPedals(2, 1),
                 [
                     ProgramChange(1, "STUDIO SET", 55),
                     ProgramChange(16, "NORD ELECTRO", 1),
                     UpperKeybInit,
                     LowerKeybInit
                 ]
                 )


def got_to_give_it_up(channel_mapping,scene):
    UpperKeybInit = initUpperKeybController(channel_mapping,scene, 1)
    LowerKeybInit = initLowerKeybController(channel_mapping,scene, 2)
    return Scene("Got to give it up",
                 Pass(),
                 [
                     ProgramChange(1, "STUDIO SET", 28),
                     ProgramChange(16, "NORD ELECTRO", 1),
                     UpperKeybInit,
                     LowerKeybInit
                 ]
                 )


def let_the_good_times_roll(channel_mapping,scene):
    UpperKeybInit = initUpperKeybController(channel_mapping,scene, 1)
    LowerKeybInit = initLowerKeybController(channel_mapping,scene, 16)
    return Scene("Let the good times roll",
                 Pass(),
                 [
                     ProgramChange(16, "NORD ELECTRO", 5),
                     UpperKeybInit,
                     LowerKeybInit
                 ]
                 )

def some_die_young(channel_mapping,scene):
    UpperKeybInit = initUpperKeybController(channel_mapping,scene, 1)
    LowerKeybInit = initLowerKeybController(channel_mapping,scene, 2)
    return Scene("Some die young",
                 Pass(),
                 [
                     ProgramChange(1, "STUDIO SET", 52),
                     ProgramChange(16, "NORD ELECTRO", 1),
                     UpperKeybInit,
                     LowerKeybInit
                 ]
                 )


def everywhere(channel_mapping,scene):
    UpperKeybInit = initUpperKeybController(channel_mapping,scene, 1)
    LowerKeybInit = initLowerKeybController(channel_mapping,scene, 2)
    return Scene("Everywhere",
                 Pass(),
                 [
                     ProgramChange(1, "STUDIO SET", 15),
                     ProgramChange(16, "NORD ELECTRO", 1),
                     UpperKeybInit,
                     LowerKeybInit
                 ]
                 )


def i_cant_stop_loving_you(channel_mapping,scene):
    UpperKeybInit = initUpperKeybController(channel_mapping,scene, 1)
    LowerKeybInit = initLowerKeybController(channel_mapping,scene, 2)
    return Scene("I can't stop loving you",
                 Pass(),
                 [
                     ProgramChange(1, "STUDIO SET", 26),
                     ProgramChange(2, "PCMS PRST", 11),
                     ProgramChange(16, "NORD ELECTRO", 1),
                     UpperKeybInit,
                     LowerKeybInit
                 ]
                 )


def aint_that_peculiar(channel_mapping,scene):
    UpperKeybInit = initUpperKeybController(channel_mapping,scene, 1)
    LowerKeybInit = initLowerKeybController(channel_mapping,scene, 16)
    return Scene("Ain't that peculiar",
                 Pass(),
                 [
                     ProgramChange(1, "STUDIO SET", 26),
                     ProgramChange(16, "NORD ELECTRO", 6),
                     UpperKeybInit,
                     LowerKeybInit
                 ]
                 )


def like_wine(channel_mapping,scene):
    UpperKeybInit = initUpperKeybController(channel_mapping,scene, 1)
    LowerKeybInit = initLowerKeybController(channel_mapping,scene, 16)
    return Scene("Like wine",
                 Pass(),
                 [
                     ProgramChange(16, "NORD ELECTRO", 9),
                     UpperKeybInit,
                     LowerKeybInit
                 ]
                 )


def as_by_stevie_wonder(channel_mapping,scene):
    name = "As"
    integra7sysex = Integra7Sysex()
    msg = integra7sysex.generateNameMsg(name)
    UpperKeybInit = initUpperKeybController(channel_mapping,scene, 1)
    LowerKeybInit = initLowerKeybController(channel_mapping,scene, 2)
    return Scene(name,
                 Pass(),
                 [
                     ProgramChange(1, "STUDIO SET", 64),
                     ProgramChange(2, "SN-A PRST", 14),
                     ProgramChange(1, "SN-S PRST", 977),
                     SysEx(msg),
                     ProgramChange(16, "NORD ELECTRO", 1),
                     UpperKeybInit,
                     LowerKeybInit
                 ]
                 )


def higher_ground(channel_mapping,scene):
    UpperKeybInit = initUpperKeybController(channel_mapping,scene, 1)
    LowerKeybInit = initLowerKeybController(channel_mapping,scene, 16)
    return Scene("Higher ground",
                 Pass(),
                 [
                     ProgramChange(1, "STUDIO SET", 45),
                     ProgramChange(16, "NORD ELECTRO", 6),
                     UpperKeybInit,
                     LowerKeybInit
                 ]
                 )


def lets_go_crazy(channel_mapping,scene):
    UpperKeybInit = initUpperKeybController(channel_mapping,scene, 1)
    LowerKeybInit = initLowerKeybController(channel_mapping,scene, 2)
    return Scene("Let's go crazy",
                 Pass(),
                 [
                     ProgramChange(1, "STUDIO SET", 56),
                     ProgramChange(16, "NORD ELECTRO", 1),
                     UpperKeybInit,
                     LowerKeybInit
                 ]
                 )
def locked_out_of_heaven(channel_mapping,scene):
    name = "Locked out of heaven"
    integra7sysex = Integra7Sysex()
    msg = integra7sysex.generateNameMsg(name)
    UpperKeybInit = initUpperKeybController(channel_mapping,scene, 1)
    LowerKeybInit = initLowerKeybController(channel_mapping,scene, 2)
    return Scene(name,
                 Transpose(-12),
                 [
                     ProgramChange(1, "STUDIO SET", 64),
                     ProgramChange(2, "SN-S PRST", 317),
                     ProgramChange(1, "SN-S PRST", 361),
                     SysEx(msg),
                     ProgramChange(16, "NORD ELECTRO", 1),
                     UpperKeybInit,
                     LowerKeybInit
                 ]
                 )

def come_as_you_are(channel_mapping,scene):
    UpperKeybInit = initUpperKeybController(channel_mapping,scene, 1)
    LowerKeybInit = initLowerKeybController(channel_mapping,scene, 2)
    return Scene("Come as you are",
                 Pass(),
                 [
                     ProgramChange(1, "STUDIO SET", 26),
                     ProgramChange(16, "NORD ELECTRO", 1),
                     ProgramChange(2, "SN-A PRST", 34),
                     UpperKeybInit,
                     LowerKeybInit
                 ]
                 )

def where_is_the_love(channel_mapping,scene):
    UpperKeybInit = initUpperKeybController(channel_mapping,scene, 1)
    LowerKeybInit = initLowerKeybController(channel_mapping,scene, 2)
    return Scene("Where is the love",
                 Pass(),
                 [
                     ProgramChange(1, "STUDIO SET", 57),
                     ProgramChange(16, "NORD ELECTRO", 1),
                     UpperKeybInit,
                     LowerKeybInit
                 ]
                 )

def luft(channel_mapping,scene):
    UpperKeybInit = initUpperKeybController(channel_mapping,scene, 1)
    LowerKeybInit = initLowerKeybController(channel_mapping,scene, 16)
    return Scene("Luft",
                 Pass(),
                 [
                     ProgramChange(1, "STUDIO SET", 60),
                     ProgramChange(16, "NORD ELECTRO", 1),
                     UpperKeybInit,
                     LowerKeybInit
                 ]
                 )

def utan_dig(channel_mapping,scene):
    UpperKeybInit = initUpperKeybController(channel_mapping,scene, 1)
    LowerKeybInit = initLowerKeybController(channel_mapping,scene, 2)
    return Scene("Utan dig",
                 Pass(),
                 [
                     ProgramChange(1, "STUDIO SET", 60),
                     ProgramChange(16, "NORD ELECTRO", 1),
                     UpperKeybInit,
                     LowerKeybInit
                 ]
                 )
