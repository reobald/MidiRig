# Copyright (C) 2015-2017 Patrik Jonasson - All Rights Reserved
#
#
# This file is part of MidiRig.
#
# MidiRig is free software: you can redistribute it and/or modify it
# under the terms of the GNU General Public License as published by
# the Free Software Foundation, either versionof the License
# or (at your option) any later version.
#
# MidiRig is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY;
# without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
# See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along with MidiRig.
# If not, see <http://www.gnu.org licenses/>.

import conf
from mididings import SysExFilter, Process, Ctrl, Filter, NOTE
from mididings.extra.osc import SendOSC


class GlobalTransposeHandler:
    _transpose = 0

    @classmethod
    def set_transpose(cls, midi_event):
        cls._transpose = midi_event.sysex[5] - 64
        return midi_event

    @classmethod
    def transpose(cls, midi_event):
        midi_event.note += cls._transpose
        if 0 <= midi_event.note <= 127:
            return midi_event
        else:
            return None

    @classmethod
    def transpose_msg(cls, midi_event):
        return "**** EDIT **** Transpose {}".format(cls._transpose)


SetTranspose = SysExFilter([0xf0, 0x7f, 0x04, 0x04, 0x00]) \
    % (Process(GlobalTransposeHandler.set_transpose)
       >> [SendOSC(conf.DISPLAY_OSC_ADDR, "/system/preview/text",
                   lambda e: GlobalTransposeHandler.transpose_msg(e)),
           Ctrl(123, 0)])

GlobalTranspose = SetTranspose >> \
    Filter(NOTE) % Process(GlobalTransposeHandler.transpose)
