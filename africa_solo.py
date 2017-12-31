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
# MidiRig is distributed in the hope that it will be useful, but WITHOUT ANY     WARRANTY;
# without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PART    ICULAR PURPOS$
# See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along wi    th MidiRig.
# If not, see <http://www.gnu.org licenses/>.

from mididings.event import MidiEvent
from mididings import NOTEON,NOTEOFF,Process

class AfricaSolo:
    _current_index = 0
    _key_list = [0, 0, 0, 0]
    _harmony_part_on = True
    _toggle_off_keys = set([73, 73, 68, 68])
    _toggle_on_keys = set([57, 57, 61, 61])
    _harmony_mapping = {
        87: 83,
        85: 80,
        83: 78,
        80: 75,
        78: 73,
        75: 71,
        73: 68,
        71: 66,
        68: 63}

    @classmethod
    def reset(cls,midi_event):
        cls._current_index = 0
        cls._key_list = [0, 0, 0, 0]
        cls._harmony_part_on = True

    @classmethod
    def _register_key(cls,midi_event):
        if midi_event.type == NOTEOFF:
            cls._key_list[cls._current_index] = midi_event.note
            cls._increment_index()
        return midi_event

    @classmethod
    def _increment_index(cls):
        cls._current_index = (AfricaSolo._current_index+1)&3

    @classmethod
    def _generate_harmony_part(cls,midi_event):
        if midi_event.type not in [NOTEON, NOTEOFF]:
            return midi_event
        if midi_event.note not in cls._harmony_mapping.keys():
            return midi_event
        events = [midi_event]
        if cls._harmony_part_on:
            note = cls._harmony_mapping.get(midi_event.note,
                                             midi_event.note)
            midi_event2 = MidiEvent(
                midi_event.type,
                midi_event.port,
                midi_event.channel,
                note,
                midi_event.velocity)
            events.append(midi_event2)
        return events

    @classmethod
    def _toggle_harmony_part(cls):
        if set(cls._key_list) == cls._toggle_off_keys:
            cls._harmony_part_on = False
        elif set(cls._key_list) == cls._toggle_on_keys:
            cls._harmony_part_on = True

    @classmethod
    def add_part(cls,midi_event):
        cls._register_key(midi_event)
        events = cls._generate_harmony_part(midi_event)
        cls._toggle_harmony_part()
        return events

def ResetAfricaSolo():
    return Process(AfricaSolo.reset)

def HarmonizeAfricaSolo():
    return Process(AfricaSolo.add_part)
