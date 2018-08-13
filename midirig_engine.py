#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright (C) 2015-2017 Patrik Jonasson - All Rights Reserved 
#
#
# This file is part of MidiRig.
#
# MidiRig is free software: you can redistribute it and/or modify it  
# under the terms of the GNU General Public License as published by  
# the Free Software Foundation, either version 3 of the License,  
# or (at your option) any later version. 
#
# MidiRig is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY;
# without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
# See the GNU General Public License for more details. 
#
# You should have received a copy of the GNU General Public License along with MidiRig.
# If not, see <http://www.gnu.org licenses/>. 


import sys
import signal
import scene
import conf
from mididings import *
from mididings.extra.gm import *
from mididings.extra.osc import OSCInterface
from mididings.extra.osc import SendOSC
from mididings.extra import *
from mididings.event import NoteOffEvent, CtrlEvent
from blinkingled import BlinkingLed
from channelmapping import ChannelMapping
from arturiamapping import ArturiaMapping
from constants import *
from global_transpose import GlobalTranspose
#=================================
# setup midiactivity indicator led
#=================================
MIDIACTIVITY_LED_PIN = 25

led = BlinkingLed(MIDIACTIVITY_LED_PIN)
led.start()

# the method that gets called at a midi event


def midiactivity(midi_event):
    led.blink()
    return midi_event

# create handler for graceful exit


def handler(signum, frame):
    led.stop_event.set()
    print 'Exiting MidiRig'
    sys.exit()


# attachhandler to system signals
signal.signal(signal.SIGTERM, handler)
signal.signal(signal.SIGINT, handler)


#=================================
# Configure MIDI environment
#=================================
config(
    # use ALSA as backend
    backend='alsa',
    # set ALSA client name
    client_name='MidiRig',
    # name ports and connect them to alsa client
    in_ports=[
        (DEFAULT_PORT, 'Virtual Raw MIDI 0-0.*:0'),
        (KEYLAB_PORT, 'KeyLab 61.*:0'),
        (INTEGRA7_PORT, 'INTEGRA-7.*:0'),
        (MIDIRIG_DISPLAY_PORT, 'MidiRigDisplay.*:0')
    ],
    out_ports=[
        (DEFAULT_PORT, 'Virtual Raw MIDI 0-0.*:0'),
        (KEYLAB_PORT, 'KeyLab 61.*:0'),
        (INTEGRA7_PORT, 'INTEGRA-7.*:0')
    ],
    # ...or just change the number of ports available    #in_ports=2,

    # when using a patchbay like QjackCtl, a small delay allows ports to be
    # connected before any MIDI events are sent
    # start_delay=0.5,
)


#================================================
# Setup midi channel translation infrastructure
#================================================
ch_map = ChannelMapping(lower_source_ch=2, upper_source_ch=1)
TranslateChannel = Process(ch_map.translate_ch)
PgcChannelMapping = Process(ch_map.pgc_channel_mapping)
ArturiaChannelMapping = Process(ch_map.arturia_channel_mapping)
RegNoteOn = Process(ch_map.reg_note_on)
HandleNoteOff = Process(ch_map.handle_note_off)
RegSusOn = Process(ch_map.reg_sus_on)
HandleSustainOff = Process(ch_map.handle_sustain_off)

#=================================
# Configure OSC communication
#=================================
port = conf.MIDIRIG_OSC_ADDR
notify_ports = (
        conf.DISPLAY_OSC_ADDR, 
        conf.TABLET_OSC_ADDR,
        conf.PHONE_OSC_ADDR)
hook(
    OSCInterface(port, notify_ports),
    ch_map
)

#================================================
# Setup arturia controller number mappings
#================================================
osc_port = conf.DISPLAY_OSC_ADDR
osc_prev_addr = "/system/preview/scene"
arturia_map = ArturiaMapping()
Arturia = (
    SysExFilter(
        manufacturer=(
            0x00,
            0x20,
            0x6B)) | ChannelFilter(1)) % (Process(
                arturia_map.return_mapping) >> CtrlFilter(
                    arturia_map.PRESET_CTRL_NR) % (SceneSwitch(
                        number=EVENT_DATA2) >> Discard()) >> CtrlFilter(
                            arturia_map.BROWSE_CTRL_NR) % (SendOSC(
                                osc_port,
                                osc_prev_addr,
                                lambda evt: evt.data2) >> Discard()))
#================================================
# All notes off - because ctrl 123 is not implemented by nord
# and also a all notes off message should send note off on all channels
# not only one channel
#================================================


def all_notes_off(midi_event):
    if midi_event.type == CTRL and midi_event.ctrl == 123:
        notes = []
        for ch in range(1, 17):
            notes.append(CtrlEvent(midi_event.port, ch, 123, 0))
        for ch in range(15, 17):
            for note in range(29, 102):
                notes.append(NoteOffEvent(midi_event.port, ch, note, 0))
            notes.append(CtrlEvent(midi_event.port, ch, 64, 0))
        return notes
    return midi_event




# cc82 always on ch 16
cc82ch16 = CtrlFilter(82) % Channel(16)

# PRE: signal midiactivity, perform arturia controller mappings and
# channelmappings
pre = Print("pre") \
    >> Process(midiactivity) >> Arturia >> Print("in")  \
    >> PgcChannelMapping >> ArturiaChannelMapping >> TranslateChannel  \
    >> RegNoteOn >> RegSusOn >> HandleNoteOff >> HandleSustainOff  \
    >> cc82ch16 >> GlobalTranspose >> Process(all_notes_off)

# CONTROL: select only program changes
#control	= Filter(PROGRAM)
control = Discard()

# POST    : log and redirect to a port
post = PortSplit({
        KEYLAB_PORT:            Port(INTEGRA7_PORT),
        INTEGRA7_PORT:          Port(INTEGRA7_PORT),
        DEFAULT_PORT:           Port(KEYLAB_PORT),
        MIDIRIG_DISPLAY_PORT:   Port(KEYLAB_PORT)})\
        >> Print("out")


#######################################################
# Scenes section
#######################################################
run(
    scenes={
        1: scene.default( ch_map, 1),
        2: scene.beautiful_day( ch_map, 2),
        3: scene.andetag( ch_map, 3),
        4: scene._24_k_magic( ch_map, 4),
        5: scene.africa( ch_map, 5),
        6: scene.evelina( ch_map, 6),
        7: scene.bara_minnen( ch_map, 7),
        8: scene.det_stora_blaa( ch_map, 8),
        9: scene.vargar( ch_map, 9),
        10: scene.angelina( ch_map, 10),
        11: scene.precis_som_forr( ch_map, 11),
        12: scene.roda_lappar( ch_map, 12),
        13: scene.anglars_tarar( ch_map, 13),
        14: scene.closer( ch_map, 14),
        15: scene.timberlake( ch_map, 15),
        16: scene.you_should_be_dancing( ch_map, 16),
        17: scene.on_my_own( ch_map, 17),
        18: scene.paradise( ch_map, 18),
        19: scene.beautiful_day( ch_map, 19),
        20: scene.sledgehammer( ch_map, 20),
        21: scene.born_to_run( ch_map, 21),
        22: scene.human_nature( ch_map, 22),
        23: scene.billie_jean( ch_map, 23),
        24: scene.staying_alive( ch_map, 24),
        25: scene.play_that_funky_music( ch_map, 25),
        26: scene.lets_go_crazy( ch_map, 26),
        27: scene.brass_octave( ch_map, 27),
        28: scene.everybody_wants_to_rule_the_world( ch_map, 28),
        29: scene.i_wish( ch_map, 29),
        30: scene.could_you_be_loved( ch_map, 30),
        31: scene.what_a_fool_believes( ch_map, 31),
        32: scene.baby_love( ch_map, 32),
        33: scene.use_me( ch_map, 33),
        34: scene.sharp_dressed_man( ch_map, 34),
        35: scene.do_i_do( ch_map, 35),
        36: scene.boys_of_summer( ch_map, 36),
        37: scene.neo_soul( ch_map, 37),
        38: scene.crazy( ch_map, 38),
        39: scene.happy( ch_map, 39),
        40: scene.i_keep_forgetting( ch_map, 40),
        41: scene.driven_to_tears( ch_map, 41),
        42: scene.i_cant_go_for_that( ch_map, 42),
        43: scene.wurlitzer( ch_map, 43),
        44: scene.make_it_right( ch_map, 44),
        45: scene.call_me_al( ch_map, 45),
        46: scene.the_way_you_make_me_feel( ch_map, 46),
        47: scene.teardrops( ch_map, 47),
        48: scene.watcha_gonna_do( ch_map, 48),
        49: scene.im_every_woman( ch_map, 49),
        50: scene.aint_nobody( ch_map, 50),
        51: scene.appaloosa( ch_map, 51),
        52: scene.in_the_air_tonight( ch_map, 52),
        53: scene.hard_to_handle( ch_map, 53),
        54: scene.land_of_confusion( ch_map, 54),
        55: scene.pick_up_the_pieces( ch_map, 55),
        56: scene.you_cant_hide_love( ch_map, 56),
        57: scene.got_to_give_it_up( ch_map, 57),
        58: scene.let_the_good_times_roll( ch_map, 58),
        59: scene.some_die_young( ch_map, 59),
        60: scene.everywhere( ch_map, 60),
        61: scene.i_cant_stop_loving_you( ch_map, 61),
        62: scene.aint_that_peculiar( ch_map, 62),
        63: scene.like_wine( ch_map, 63),
        64: scene.as_by_stevie_wonder( ch_map, 64),
        65: scene.higher_ground( ch_map, 65),
        66: scene.locked_out_of_heaven(ch_map,66),
        67: scene.where_is_the_love(ch_map,67),
        68: scene.come_as_you_are(ch_map,68),
        69: scene.luft(ch_map,69),
        70: scene.utan_dig(ch_map,70),
    },
    control=control,
    pre=pre,
    post=post
)
