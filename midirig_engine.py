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
      (DEFAULT_IN_PORT, 'Virtual Raw MIDI 0-0.*:0'),
      (KEYLAB_IN_PORT, 'KeyLab.*:0'),
      (INTEGRA7_IN_PORT, 'INTEGRA-7.*:0'),
      (MIDIRIG_DISPLAY_IN_PORT, 'MidiRigDisplay.*:0')
    ],
    out_ports=[
        (KEYLAB_OUT_PORT, 'KeyLab 61.*:0'),
        (INTEGRA7_OUT_PORT, 'INTEGRA-7.*:0'),
    ],
    # ...or just change the number of ports available    #in_ports=2,

    # when using a patchbay like QjackCtl, a small delay allows ports to be
    # connected before any MIDI events are sent
    # start_delay=0.5,
)


#=================================
# Configure OSC communication
#=================================
port = sys.argv[1]
notify_ports = sys.argv[2:]
hook(
    OSCInterface(port, notify_ports)
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

#================================================
# Setup arturia controller number mappings
#================================================
osc_port = sys.argv[2]
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


#================================================
# Setup transpose infrastructure
#================================================
transpose = 0


def set_transpose(midi_event):
    global transpose
    transpose = midi_event.sysex[5] - 64
    return midi_event


def global_transpose(midi_event):
    midi_event.note += transpose
    if 0 <= midi_event.note <= 127:
        return midi_event
    else:
        return None


def transpose_msg(midi_event):
    global transpose
    return "**** EDIT **** Transpose {}".format(transpose)


SetTranspose = SysExFilter([0xf0, 0x7f, 0x04, 0x04, 0x00]) \
    % (Process(set_transpose)
       >> [SendOSC(56419, "/system/preview/text", lambda e: transpose_msg(e)), Ctrl(123, 0)])
GlobalTranspose = Filter(NOTE) % Process(global_transpose)


# cc82 always on ch 16
cc82ch16 = CtrlFilter(82) % Channel(16)

# PRE: signal midiactivity, perform arturia controller mappings and
# channelmappings
pre = Print("pre") \
    >> Process(midiactivity) >> Arturia >> Print("in")  \
    >> PgcChannelMapping >> ArturiaChannelMapping >> TranslateChannel  \
    >> RegNoteOn >> RegSusOn >> HandleNoteOff >> HandleSustainOff  \
    >> cc82ch16 >> SetTranspose >> GlobalTranspose >> Process(all_notes_off)

# CONTROL: select only program changes
#control	= Filter(PROGRAM)
control = Discard()

# POST    : log and redirect to a port
post = Print("out")  \
    >> [SysExFilter(manufacturer=(0x00, 0x20, 0x6B))
        % Port(KEYLAB_OUT_PORT), Port(INTEGRA7_OUT_PORT)]


#######################################################
# Scenes section
#######################################################
run(
    scenes={
        1: scene.default(),
        2: scene.beautiful_day(),
        3: scene.andetag(),
        4: scene._24_k_magic(),
        5: scene.africa(),
        6: scene.evelina(),
        7: scene.bara_minnen(),
        8: scene.det_stora_blaa(),
        9: scene.vargar(),
        10: scene.angelina(),
        11: scene.precis_som_forr(),
        12: scene.roda_lappar(),
        13: scene.anglars_tarar(),
        14: scene.closer(),
        15: scene.timberlake(),
        16: scene.you_should_be_dancing(),
        17: scene.on_my_own(),
        18: scene.paradise(),
        19: scene.beautiful_day(),
        20: scene.sledgehammer(),
        21: scene.born_to_run(),
        22: scene.human_nature(),
        23: scene.billie_jean(),
        24: scene.staying_alive(),
        25: scene.play_that_funky_music(),
        26: scene.lets_go_crazy(),
        27: scene.brass_octave(),
        28: scene.everybody_wants_to_rule_the_world(),
        29: scene.i_wish(),
        30: scene.could_you_be_loved(),
        31: scene.what_a_fool_believes(),
        32: scene.baby_love(),
        33: scene.use_me(),
        34: scene.sharp_dressed_man(),
        35: scene.do_i_do(),
        36: scene.boys_of_summer(),
        37: scene.neo_soul(),
        38: scene.crazy(),
        39: scene.happy(),
        40: scene.i_keep_forgetting(),
        41: scene.driven_to_tears(),
        42: scene.i_cant_go_for_that(),
        43: scene.wurlitzer(),
        44: scene.make_it_right(),
        45: scene.call_me_al(),
        46: scene.the_way_you_make_me_feel(),
        47: scene.teardrops(),
        48: scene.watcha_gonna_do(),
        49: scene.im_every_woman(),
        50: scene.aint_nobody(),
        51: scene.appaloosa(),
        52: scene.in_the_air_tonight(),
        53: scene.hard_to_handle(),
        54: scene.land_of_confusion(),
        55: scene.pick_up_the_pieces(),
        56: scene.you_cant_hide_love(),
        57: scene.got_to_give_it_up(),
        58: scene.let_the_good_times_roll(),
        59: scene.some_die_young(),
        60: scene.everywhere(),
        61: scene.i_cant_stop_loving_you(),
        62: scene.aint_that_peculiar(),
        63: scene.like_wine(),
        64: scene.as_by_stevie_wonder(),
        65: scene.higher_ground(),
    },
    control=control,
    pre=pre,
    post=post
)
