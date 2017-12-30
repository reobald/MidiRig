from mididings import *
from customunits import ProgramChange,ConvertExpression, ConnectSusPedals
from mididings.extra import *
from roland_sysex import Integra7Sysex
from mididings.event import MidiEvent

def default():
    return Scene("Default",
                Pass(),
                [
                    ProgramChange(1, "STUDIO SET", 25),
                    ProgramChange(16, "NORD ELECTRO", 1)
                ]
                )


def beautiful_day():
    return Scene("Beautiful day",
                 Pass(),
                 [
                     ProgramChange(1, "STUDIO SET", 1),
                     ProgramChange(16, "NORD ELECTRO", 1)
                 ]
                 )


def andetag():
    return Scene("Andetag",
                 Pass(),
                 [
                     ProgramChange(1, "STUDIO SET", 2),
                     ProgramChange(16, "NORD ELECTRO", 1)
                 ]
                 )


def good_riddance():
    return Scene("Good riddance",
                 Pass(),
                 [
                     ProgramChange(1, "STUDIO SET", 3),
                     ProgramChange(16, "NORD ELECTRO", 1)
                 ]
                 )

africa_keyswitch = [0,0,0,0,0]
africa_part_on = True
def africa():
    solo_part = {
        87:83,
        85:80,
        83:78,
        80:75,
        78:73,
        75:71,
        73:68,
        71:66,
        68:63}

    def reset_globals(midi_event):
        print "reset globals"
        global africa_keyswitch
        global africa_part_on
        africa_keyswitch = [0,0,0,0,0]
        africa_part_on = True

    def reg_key(midi_event):
        global africa_keyswitch
        if midi_event.type == NOTEOFF:
            index = africa_keyswitch[4]
            africa_keyswitch[index] = midi_event.note
            africa_keyswitch[4]=(index+1)&3
            print "reg_key: {}".format(africa_keyswitch)
        return midi_event

    def generate_solo_part(midi_event):
        global africa_keyswitch
        global africa_part_on
        events = [midi_event]
        if africa_part_on:
            midi_event2 = MidiEvent(midi_event.type, 
                                    midi_event.port,
                                    midi_event.channel,
                                    solo_part.get(
                                        midi_event.note,
                                        midi_event.note),
                                    midi_event.velocity)
            events.append(midi_event2)
        switch_off_value = 282 # 73+73+68+68
        switch_on_value = 236 # 57+57+61+61
        checksum = sum(africa_keyswitch[0:4])
        print  africa_keyswitch       
        if checksum == switch_off_value:
            africa_part_on = False
            print "africa switch off"
        elif checksum == switch_on_value:
            africa_part_on = True
            print "africa switch off"
        return events

    def SoloPart():
        return (ChannelFilter(4) & \
                KeyFilter(notes=[87,85,83,80,78,75,73,71,68,57,61])) %\
                Process(generate_solo_part)
                 
    return Scene("Africa",
                Process(reg_key)>>SoloPart(),
                 [
                     Process(reset_globals),
                     ProgramChange(1, "STUDIO SET", 4),
                     ProgramChange(16, "NORD ELECTRO", 1)
                 ]
                ) 


def evelina():
    return Scene("Evelina", 
                  (ChannelFilter(4) & CtrlFilter(11)) % \
                   ConvertExpression(4, 74) >> \
                   CtrlRange(74, 20, 120), 
                   [
                        ProgramChange(1, "STUDIO SET", 5), 
                        ProgramChange(16, "NORD ELECTRO", 1)
                   ]
                )


def bara_minnen():
    return Scene("Bara minnen",
                 Pass(),
                 [
                     ProgramChange(1, "STUDIO SET", 6),
                     ProgramChange(16, "NORD ELECTRO", 16)
                 ]
                 )


def det_stora_blaa():
    return Scene("Det stora blaa",
                 Pass(),
                 [
                     ProgramChange(1, "STUDIO SET", 7),
                     ProgramChange(16, "NORD ELECTRO", 1)
                 ]
                 )


def vargar():
    return Scene("Vargar",
                 Pass(),
                 [
                     ProgramChange(1, "STUDIO SET", 8),
                     ProgramChange(16, "NORD ELECTRO", 1)
                 ]
                 )


def angelina():
    return Scene("Angelina",
                 Pass(),
                 [
                     ProgramChange(1, "STUDIO SET", 9),
                     ProgramChange(16, "NORD ELECTRO", 1)
                 ]
                 )


def precis_som_forr():
    return Scene("Precis som forr",
                 Pass(),
                 [
                     ProgramChange(1, "STUDIO SET", 10),
                     ProgramChange(16, "NORD ELECTRO", 1)
                 ]
                 )


def roda_lappar():
    return Scene("Roda lappar",
                 Pass(),
                 [
                     ProgramChange(1, "STUDIO SET", 11),
                     ProgramChange(16, "NORD ELECTRO", 1)
                 ]
                 )


def anglars_tarar():
    return Scene("Anglars tarar",
                 Pass(),
                 [
                     ProgramChange(1, "STUDIO SET", 12),
                     ProgramChange(16, "NORD ELECTRO", 1)
                 ]
                 )


def closer():
    return Scene("Closer",
                 Pass(),
                 [
                     ProgramChange(1, "STUDIO SET", 13),
                     ProgramChange(16, "NORD ELECTRO", 1)
                 ]
                 )


def timberlake():
    return Scene("Timberlake",
                 CtrlRange(11, 127, 80) >> CtrlFilter(
                     11) % [Pass(), Channel(1)],
                 [
                     ProgramChange(1, 'STUDIO SET', 14),
                     ProgramChange(16, 'NORD ELECTRO', 1),
                 ]
                 )


def you_should_be_dancing():
    name = "U shld B dancing"
    integra7sysex = Integra7Sysex()
    msg = integra7sysex.generateNameMsg(name)
    return Scene("You should be dancing",
                 Pass(),
                 [
                     ProgramChange(1, "STUDIO SET", 64),
                     ProgramChange(2, "SN-A USER", 10),
                     ProgramChange(3, "PCMS PRST", 612),
                     ProgramChange(1, "SN-A PRST", 206),
                     SysEx(msg),
                     ProgramChange(16, "NORD ELECTRO", 1)
                 ]
                 )


def on_my_own():
    name = "On my own"
    integra7sysex = Integra7Sysex()
    msg = integra7sysex.generateNameMsg(name)
    return Scene(name,
                 Pass(),
                 [
                     ProgramChange(1, "STUDIO SET", 64),
                     ProgramChange(16, "NORD ELECTRO", 12),
                     ProgramChange(1, "SN-S PRST", 425),
                     SysEx(msg)
                 ]
                 )


def paradise():
    return Scene("Paradise",
                 Pass(),
                 [
                     ProgramChange(1, "STUDIO SET", 17),
                     ProgramChange(16, "NORD ELECTRO", 1)
                 ]
                 )


def beautiful_day():
    return Scene("Beautiful day",
                 Pass(),
                 [
                     ProgramChange(1, "STUDIO SET", 1),
                     ProgramChange(16, "NORD ELECTRO", 1)
                 ]
                 )


def sledgehammer():
    return Scene("SledgeHammer",
                 Pass(),
                 [
                     ProgramChange(1, "STUDIO SET", 19),
                     ProgramChange(16, "NORD ELECTRO", 1)
                 ]
                 )


def born_to_run():
    return Scene("Born to Run",
                 Pass(),
                 [
                     ProgramChange(1, "STUDIO SET", 20),
                     ProgramChange(16, "NORD ELECTRO", 1)
                 ]
                 )


def human_nature():
    return Scene("Human Nature",
                 ConnectSusPedals(2, 1),
                 [
                     ProgramChange(1, "STUDIO SET", 21),
                     ProgramChange(16, "NORD ELECTRO", 1)
                 ]
                 )


def billie_jean():
    return Scene("Billie Jean",
                 CtrlFilter(82) % SceneSwitch(number=44),
                 [
                     ProgramChange(1, "STUDIO SET", 22),
                     ProgramChange(16, "NORD ELECTRO", 1)
                 ]
                 )


def staying_alive():
    name = "Staying alive"
    integra7sysex = Integra7Sysex()
    msg = integra7sysex.generateNameMsg(name)
    return Scene(name,
                 Pass(),
                 [
                     ProgramChange(1, "STUDIO SET", 64),
                     ProgramChange(2, "SN-A PRST", 10),
                     ProgramChange(1, "SN-A PRST", 208),
                     SysEx(msg),
                     ProgramChange(16, "NORD ELECTRO", 1)
                 ]
                 )


def play_that_funky_music():
    return Scene("Play That Funky Music",
                 Pass(),
                 [
                     ProgramChange(1, "STUDIO SET", 24),
                     ProgramChange(16, "NORD ELECTRO", 6)
                 ]
                 )


def brass_octave():
    return Scene("Brass Octave",
                 Pass(),
                 [
                     ProgramChange(1, "STUDIO SET", 26),
                     ProgramChange(16, "NORD ELECTRO", 1)
                 ]
                 )


def everybody_wants_to_rule_the_world():
    return Scene("Everybody wants to rule the world",
                 Pass(),
                 [
                     ProgramChange(1, "STUDIO SET", 27),
                     ProgramChange(16, "NORD ELECTRO", 1)
                 ]
                 )


def i_wish():
    return Scene("I Wish",
                 Pass(),
                 [
                     ProgramChange(1, "STUDIO SET", 28),
                     ProgramChange(16, "NORD ELECTRO", 1)
                 ]
                 )


def could_you_be_loved():
    return Scene("Could You Be Loved",
                 Pass(),
                 [
                     ProgramChange(1, "STUDIO SET", 29),
                     ProgramChange(16, "NORD ELECTRO", 4)
                 ]
                 )


def what_a_fool_believes():
    return Scene("What a Fool Believes",
                 Pass(),
                 [
                     ProgramChange(1, "STUDIO SET", 30),
                     ProgramChange(16, "NORD ELECTRO", 1)
                 ]
                 )


def baby_love():
    return Scene("Baby Love",
                 Pass(),
                 [
                     ProgramChange(1, "STUDIO SET", 31),
                     ProgramChange(16, "NORD ELECTRO", 6)
                 ]
                 )


def use_me():
    return Scene("Use Me",
                 Pass(),
                 [
                     ProgramChange(1, "STUDIO SET", 32),
                     ProgramChange(16, "NORD ELECTRO", 6)
                 ]
                 )


def sharp_dressed_man():
    return Scene("Sharp Dressed Man",
                 Pass(),
                 [
                     ProgramChange(1, "STUDIO SET", 33),
                     ProgramChange(16, "NORD ELECTRO", 1)
                 ]
                 )


def do_i_do():
    return Scene("Do I Do",
                 Pass(),
                 [
                     ProgramChange(1, "STUDIO SET", 34),
                     ProgramChange(16, "NORD ELECTRO", 1)
                 ]
                 )


def boys_of_summer():
    return Scene("Boys Of Summer",
                 ConvertExpression(2, 74) >> CtrlRange(74, 60, 120),
                 [
                     ProgramChange(1, "STUDIO SET", 35),
                     ProgramChange(16, "NORD ELECTRO", 1)
                 ]
                 )


def neo_soul():
    return Scene("Neo Soul",
                 Pass(),
                 [
                     ProgramChange(1, "STUDIO SET", 36),
                     ProgramChange(16, "NORD ELECTRO", 1)
                 ]
                 )


def crazy():
    return Scene("Crazy",
                 Pass(),
                 [
                     ProgramChange(1, "STUDIO SET", 37),
                     ProgramChange(16, "NORD ELECTRO", 1)
                 ]
                 )


def happy():
    return Scene("Happy",
                 Pass(),
                 [
                     ProgramChange(1, "STUDIO SET", 38),
                     ProgramChange(16, "NORD ELECTRO", 3)
                 ]
                 )


def i_keep_forgetting():
    return Scene("I Keep Forgetting",
                 Pass(),
                 [
                     ProgramChange(1, "STUDIO SET", 39),
                     ProgramChange(16, "NORD ELECTRO", 1)
                 ]
                 )


def driven_to_tears():
    return Scene("Driven to Tears",
                 Pass(),
                 [
                     ProgramChange(1, "STUDIO SET", 40),
                     ProgramChange(16, "NORD ELECTRO", 1)
                 ]
                 )


def i_cant_go_for_that():
    return Scene("I Can't Go For That",
                 Pass(),
                 [
                     ProgramChange(1, "STUDIO SET", 41),
                     ProgramChange(16, "NORD ELECTRO", 1)
                 ]
                 )


def wurlitzer():
    name = "Wurlitzer"
    integra7sysex = Integra7Sysex()
    msg = integra7sysex.generateNameMsg(name)
    return Scene(name,
                 Pass(),
                 [
                     ProgramChange(1, "STUDIO SET", 64),
                     ProgramChange(2, "SN-A PRST", 32),
                     SysEx(msg),
                     ProgramChange(16, "NORD ELECTRO", 1)
                 ]
                 )


def make_it_right():
    return Scene("Make It Right",
                 Pass(),
                 [
                     ProgramChange(1, "STUDIO SET", 43),
                     ProgramChange(16, "NORD ELECTRO", 1)
                 ]
                 )


def call_me_al():
    return Scene("Call Me Al",
                 Pass(),
                 [
                     ProgramChange(1, "STUDIO SET", 44),
                     ProgramChange(16, "NORD ELECTRO", 1)
                 ]
                 )


def the_way_you_make_me_feel():
    return Scene("The Way You Make Me Feel",
                 Pass(),
                 [
                     ProgramChange(1, "STUDIO SET", 45),
                     ProgramChange(16, "NORD ELECTRO", 6)
                 ]
                 )


def teardrops():
    return Scene("Teardrops",
                 Pass(),
                 [
                     ProgramChange(1, "STUDIO SET", 46),
                     ProgramChange(16, "NORD ELECTRO", 1)
                 ]
                 )


def watcha_gonna_do():
    return Scene("Watcha Gonna Do",
                 Pass(),
                 [
                     ProgramChange(1, "STUDIO SET", 47),
                     ProgramChange(16, "NORD ELECTRO", 1)
                 ]
                 )


def im_every_woman():
    return Scene("I'm Every Woman",
                 Pass(),
                 [
                     ProgramChange(1, "STUDIO SET", 48),
                     ProgramChange(16, "NORD ELECTRO", 1)
                 ]
                 )


def aint_nobody():
    return Scene("Ain't Nobody",
                 ChannelFilter(2) % CtrlMap(11, 74),
                 [
                     ProgramChange(1, "STUDIO SET", 49),
                     ProgramChange(16, "NORD ELECTRO", 1)
                 ]
                 )


def appaloosa():
    name = "Appaloosa"
    integra7sysex = Integra7Sysex()

    nameChange = integra7sysex.generateNameMsg(name)

    part = 3
    channel = 1
    part3ChannelChange = integra7sysex.generateChannelChangeMsg(part, channel)

    part = 2
    volume = 118
    part2VolumeChange = integra7sysex.generateVolumeChangeMsg(part, volume)

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
                     ProgramChange(16, "NORD ELECTRO", 1)
                 ]
                 )


def in_the_air_tonight():
    ifExprOnMidiCh2 = (ChannelFilter(2) & CtrlFilter(11))
    ifChannel2 = ChannelFilter(2)
    return Scene("In the Air Tonight", 
                ifExprOnMidiCh2 % \
                (Channel(3) >> \
                CtrlMap( 11, 74) >> \
                CtrlRange(74, 40, 127)) >> \
                ifChannel2 %
                    [ Pass(), Channel(3)], 
                    [
                        ProgramChange(1, "STUDIO SET", 51), 
                        ProgramChange(16, "NORD ELECTRO", 1)
                    ]
                    )


def cant_take_my_eyes_off_you():
    return Scene("Cant take My Eyes Off You",
                 Pass(),
                 [
                     ProgramChange(1, "STUDIO SET", 52),
                     ProgramChange(16, "NORD ELECTRO", 1)
                 ]
                 )


def land_of_confusion():
    return Scene("Land Of Confusion",
                 Pass(),
                 [
                     ProgramChange(1, "STUDIO SET", 53),
                     ProgramChange(16, "NORD ELECTRO", 1)
                 ]
                 )


def pick_up_the_pieces():
    return Scene("Pick Up The Pieces",
                 Pass(),
                 [
                     ProgramChange(1, "STUDIO SET", 54),
                     ProgramChange(16, "NORD ELECTRO", 1)
                 ]
                 )


def you_cant_hide_love():
    return Scene("You Can't Hide Love",
                 ConnectSusPedals(2, 1),
                 [
                     ProgramChange(1, "STUDIO SET", 55),
                     ProgramChange(16, "NORD ELECTRO", 1)
                 ]
                 )


def got_to_give_it_up():
    return Scene("Got to give it up",
                 Pass(),
                 [
                     ProgramChange(1, "STUDIO SET", 28),
                     ProgramChange(16, "NORD ELECTRO", 1)
                 ]
                 )


def let_the_good_times_roll():
    return Scene("Let the good times roll",
                 Pass(),
                 [
                     ProgramChange(16, "NORD ELECTRO", 5)
                 ]
                 )

def some_die_young():
    return Scene("Some die young",
                 Pass(),
                 [
                     ProgramChange(1, "STUDIO SET", 52),
                     ProgramChange(16, "NORD ELECTRO", 1)
                 ]
                 )


def everywhere():
    return Scene("Everywhere",
                 Pass(),
                 [
                     ProgramChange(1, "STUDIO SET", 15),
                     ProgramChange(16, "NORD ELECTRO", 1)
                 ]
                 )


def i_cant_stop_loving_you():
    return Scene("I can't stop loving you",
                 Pass(),
                 [
                     ProgramChange(1, "STUDIO SET", 26),
                     ProgramChange(2, "PCMS PRST", 11),
                     ProgramChange(16, "NORD ELECTRO", 1)
                 ]
                 )


def aint_that_peculiar():
    return Scene("Ain't that peculiar",
                 Pass(),
                 [
                     ProgramChange(1, "STUDIO SET", 26),
                     ProgramChange(16, "NORD ELECTRO", 6)
                 ]
                 )


def like_wine():
    return Scene("Like wine",
                 Pass(),
                 [
                     ProgramChange(16, "NORD ELECTRO", 9)
                 ]
                 )


def as_by_stevie_wonder():
    name = "As"
    integra7sysex = Integra7Sysex()
    msg = integra7sysex.generateNameMsg(name)
    return Scene(name,
                 Pass(),
                 [
                     ProgramChange(1, "STUDIO SET", 64),
                     ProgramChange(2, "SN-A PRST", 14),
                     ProgramChange(1, "SN-S PRST", 977),
                     SysEx(msg),
                     ProgramChange(16, "NORD ELECTRO", 1)
                 ]
                 )


def higher_ground():
    return Scene("Higher ground",
                 Pass(),
                 [
                     ProgramChange(1, "STUDIO SET", 45),
                     ProgramChange(16, "NORD ELECTRO", 6)
                 ]
                 )
