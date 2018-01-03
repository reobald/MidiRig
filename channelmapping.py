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


from mididings.event import MidiEvent, NoteOffEvent, CtrlEvent
from mididings import *


class ChannelMapping:
    def __init__(self, **kwargs):
        self.lower_source_ch = kwargs.get('lower_source_ch')
        self.upper_source_ch = kwargs.get('upper_source_ch')
        self.lower_dest_ch = kwargs.get('lower_source_ch')
        self.upper_dest_ch = kwargs.get('upper_source_ch')
        self.current_channel = kwargs.get('lower_source_ch')
        self.upper_keys_pressed = {}
        self.lower_keys_pressed = {}
        self.lower_sustain = {}
        self.upper_sustain = {}
        self.lower_keyb_controller_inits={}
        self.upper_keyb_controller_inits={}

    def add_upper_keyb_init(self, scene, channel):
        self.upper_keyb_controller_inits[scene]=channel
    
    
    def add_lower_keyb_init(self, scene, channel):
        self.lower_keyb_controller_inits[scene]=channel
    
    
    def on_switch_scene(self,scene, subscene):
        print "on_scene_switch@channelmapping"
        lower_ch = self.lower_keyb_controller_inits.get(scene,2)
        upper_ch = self.upper_keyb_controller_inits.get(scene,1)
        self.change_lower_channel_mapping(lower_ch) 
        self.change_upper_channel_mapping(upper_ch) 


    def translate_ch(self, midi_event):
        if (midi_event.channel == self.upper_source_ch):
            midi_event.channel = self.upper_dest_ch
        elif (midi_event.channel == self.lower_source_ch):
            midi_event.channel = self.lower_dest_ch
        return midi_event

    def change_upper_channel_mapping(self, ch):
        self.upper_dest_ch = ch

    def change_lower_channel_mapping(self, ch):
        self.lower_dest_ch = ch


    def pgc_channel_mapping(self, midi_event):
        if (midi_event.type == PROGRAM):
            ch = midi_event.program % 8
            if (ch == 0):
                ch = 16
            if (ch == 7):
                ch = 15
            if(midi_event.channel == self.lower_source_ch):
                self.change_lower_channel_mapping(ch) 
            elif(midi_event.channel == self.upper_source_ch):
                self.change_upper_channel_mapping(ch) 
            return None
        return midi_event

    def arturia_channel_mapping(self, midi_event):
        if(midi_event.channel == self.upper_source_ch):
            if (midi_event.type == CTRL):
                if (22 <= midi_event.ctrl <= 29):
                    self.change_upper_dest_ch(midi_event.ctrl - 21)
                    return None
                elif (30 <= midi_event.ctrl <= 31):
                    self.change_upper_dest_ch(midi_event.ctrl - 15)
                    return None
        return midi_event

    def reg_note_on(self, midi_event):
        if midi_event.type == NOTEON:
            source_upper = midi_event.channel == self.upper_dest_ch
            source_lower = midi_event.channel == self.lower_dest_ch
            if source_lower:
                self.lower_keys_pressed[midi_event.data1] = midi_event.channel
            if source_upper:
                self.upper_keys_pressed[midi_event.data1] = midi_event.channel
        return midi_event

    def reg_sus_on(self, midi_event):
        if midi_event.type == CTRL and midi_event.ctrl == 64 and midi_event.data2 >= 64:
            source_upper = midi_event.channel == self.upper_dest_ch
            source_lower = midi_event.channel == self.lower_dest_ch
            if source_lower:
                self.lower_sustain[midi_event.data1] = midi_event.channel
            if source_upper:
                self.upper_sustain[midi_event.data1] = midi_event.channel
        return midi_event

    def handle_note_off(self, midi_event):
        event_list = [midi_event]
        if midi_event.type == NOTEOFF:
            source_upper = midi_event.channel == self.upper_dest_ch
            source_lower = midi_event.channel == self.lower_dest_ch
            key = midi_event.data1
            port = midi_event.port
            if source_lower:
                try:
                    ch = self.lower_keys_pressed.get(key)
                    event_list.append(MidiEvent(NOTEOFF, port, ch, key))
                    del self.lower_keys_pressed[key]
                except BaseException:
                    print "No previous lower key press registered"
            if source_upper:
                try:
                    ch = self.upper_keys_pressed.get(key)
                    midi_event.channel = ch
                    event_list.append(MidiEvent(NOTEOFF, port, ch, key))
                    del self.upper_keys_pressed[key]
                except BaseException:
                    print "No previous upper key press registered"
        return event_list

    def handle_sustain_off(self, midi_event):
        event_list = [midi_event]
        if midi_event.type == CTRL and midi_event.ctrl == 64 and midi_event.data2 < 64:
            source_upper = midi_event.channel == self.upper_dest_ch
            source_lower = midi_event.channel == self.lower_dest_ch
            key = midi_event.data1
            port = midi_event.port
            if source_lower:
                try:
                    ch = self.lower_sustain.get(key)
                    event_list.append(
                        MidiEvent(
                            CTRL,
                            port,
                            ch,
                            midi_event.data1,
                            midi_event.data2))
                    del self.lower_sustain[key]
                except BaseException:
                    print "No previous sustain registered"
            if source_upper:
                try:
                    ch = self.upper_sustain.get(key)
                    midi_event.channel = ch
                    event_list.append(
                        MidiEvent(
                            CTRL,
                            port,
                            ch,
                            midi_event.data1,
                            midi_event.data2))
                    del self.upper_sustain[key]
                except BaseException:
                    print "No previous sustain registered"
        return event_list
