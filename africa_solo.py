from mididings.event import MidiEvent
from mididings import *

class AfricaSoloHarmony:
    def __init__(self):
        self._current_index = 0
        self._key_list = [0, 0, 0, 0]
        self._harmony_part_on = True
        self._toggle_off_keys = set([73, 73, 68, 68])
        self._toggle_on_keys = set([57, 57, 61, 61])
        self._harmony_mapping = {
            87: 83,
            85: 80,
            83: 78,
            80: 75,
            78: 73,
            75: 71,
            73: 68,
            71: 66,
            68: 63}

    def _register_key(self, midi_event):
        if midi_event.type == NOTEOFF:
            self._key_list[self._current_index] = midi_event.note
            self._increment_index()
            print self._key_list
        return midi_event

    def _increment_index(self):
        self._current_index = (self._current_index+1)&3

    def _generate_harmony_part(self, midi_event):
        if midi_event.type not in [NOTEON, NOTEOFF]:
            return midi_event
        if midi_event.note not in self._harmony_mapping.keys():
            return midi_event
        events = [midi_event]
        if self._harmony_part_on:
            note = self._harmony_mapping.get(midi_event.note,
                                             midi_event.note)
            midi_event2 = MidiEvent(
                midi_event.type,
                midi_event.port,
                midi_event.channel,
                note,
                midi_event.velocity)
            events.append(midi_event2)
        return events

    def _toggle_harmony_part(self):
        if set(self._key_list) == self._toggle_off_keys:
            self._harmony_part_on = False
        elif set(self._key_list) == self._toggle_on_keys:
            self._harmony_part_on = True

    def add_part(self,midi_event):
        self._register_key(midi_event)
        events = self._generate_harmony_part(midi_event)
        self._toggle_harmony_part()
        return events

