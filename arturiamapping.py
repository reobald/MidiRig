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
# without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOS$
# See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along with MidiRig.
# If not, see <http://www.gnu.org licenses/>.


from mididings.event import MidiEvent, ProgramEvent, CtrlEvent, SysExEvent
from mididings import *
from mididings.extra.osc import SendOSC
import sys
from constants import DEFAULT_PORT
import arturia_sysex

class ArturiaMapping:
    def __init__(self):
        self._transpose = 64
        self._preset = 1

        self._reset_display_event = None

        self._toggle_memory = {}

        self.BROWSE_CTRL_NR = 114
        self.PRESET_CTRL_NR = 115

        self._ctrl_map = {
            12: lambda evt: CtrlEvent(evt.port, 16, 82, evt.value),
            22: lambda evt: self._convert_ctl_to_pgm(evt, 1),
            23: lambda evt: self._convert_ctl_to_pgm(evt, 2),
            24: lambda evt: self._convert_ctl_to_pgm(evt, 3),
            25: lambda evt: self._convert_ctl_to_pgm(evt, 4),
            26: lambda evt: self._convert_ctl_to_pgm(evt, 5),
            27: lambda evt: self._convert_ctl_to_pgm(evt, 6),
            28: lambda evt: self._convert_ctl_to_pgm(evt, 7),
            29: lambda evt: self._convert_ctl_to_pgm(evt, 8),
            30: lambda evt: self._convert_ctl_to_pgm(evt, 15),
            31: lambda evt: self._convert_ctl_to_pgm(evt, 16),
            53: lambda evt: self._generate_transpose_sysex_event(evt, -1),
            52: lambda evt: self._generate_transpose_sysex_event(evt, 1),
            51: lambda evt: self._generate_transpose_sysex_event(evt, 0),
            54: lambda evt: self._generate_all_notes_off_events(evt),
            55: lambda evt: self._toggle_ctrl(CtrlEvent(evt.port, 16, 82, evt.value)),
            64: lambda evt: CtrlEvent(evt.port, evt.channel, 64, 127 - evt.value),
            114: lambda evt: self._browse_presets(evt),
            115: lambda evt: self._select_preset(evt),
            118: lambda evt: self._step_preset(evt, 0),
            119: lambda evt: self._step_preset(evt, 127),
        }

    def return_mapping(self, midi_event):
        try:
            if midi_event.type == CTRL:
                return self._ctrl_map[midi_event.ctrl](midi_event)
        except KeyError:
            pass
        if arturia_sysex.is_name_msg(midi_event):
            self._reset_display_event = midi_event
        return midi_event

    def _toggle_button_lights(self, event):
        button = event.ctrl - 22
        return arturia_sysex.generateToggledButtonEvents( button )

    def _convert_ctl_to_pgm(self, midi_event, program):
        if midi_event.value > 0:
            port = midi_event.port
            channel = midi_event.channel
            return ProgramEvent(port, channel, program)
        else:
            sysex_events = self._toggle_button_lights(midi_event)
            sysex_events.append(self._reset_display_event)
            return sysex_events

    def _toggle_ctrl(self, midi_event):
        if midi_event.value > 0:
            toggle = self._toggle_memory.get(midi_event.ctrl, True)
            midi_event.value = toggle * midi_event.value
            self._toggle_memory[midi_event.ctrl] = not toggle
            return midi_event
        return None

    def _is_arturia_sysex_name_msg(self, midi_event):
        if midi_event.type == SYSEX:
            header = [0xf0, 0x00, 0x20, 0x6B, 0x7F, 0x42, 0x04, 0x00, 0x60]
            for i, b in enumerate(header):
                if b != midi_event.sysex[i]:
                    print "no match: {}!={}".format(b, midi_event.sysex[i])
                    return False
            return True
        else:
            return False

    def _browse_presets(self, midi_event):
        if midi_event.data2 < 64 and self._preset > 1:
            self._preset -= 1
        elif self._preset < 256:
            self._preset += 1
        midi_event.data2 = self._preset
        return midi_event

    def _step_preset(self, midi_event, value):
        if midi_event.data2 > 0:
            midi_event.data1 = 114
            midi_event.data2 = value
            return self._browse_presets(midi_event)
        else:
            return self._reset_display_event

    def _select_preset(self, midi_event):
        if midi_event.data2 > 0:
            midi_event.data2 = self._preset - 1
            return midi_event
        else:
            return self._reset_display_event

    def _generate_transpose_sysex_event(self, midievent, transposeValue):
        if midievent.value > 0:
            tmp = 64 if transposeValue == 0 else self._transpose + transposeValue
            if 0 <= tmp <= 127:
                self._transpose = tmp
                syx = [0xf0, 0x7f, 0x04, 0x04, 0x00, self._transpose, 0xf7]
                return SysExEvent(DEFAULT_PORT, syx)
        return self._reset_display_event

    def _generate_all_notes_off_events(self, midievent):
        if midievent.value > 0:
            note_off_events = []
            for ch in range(1, 17):
                note_off_events.append(CtrlEvent(midievent.port, ch, 123, 0))
            return note_off_events
        else:
            return self._reset_display_event
