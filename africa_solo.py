from mididings.event import MidiEvent
from mididings import *

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

    @staticmethod
    def reset(midi_event):
        AfricaSolo._current_index = 0
        AfricaSolo._key_list = [0, 0, 0, 0]
        AfricaSolo._harmony_part_on = True

    @staticmethod
    def _register_key(midi_event):
        if midi_event.type == NOTEOFF:
            AfricaSolo._key_list[AfricaSolo._current_index] = midi_event.note
            AfricaSolo._increment_index()
            print AfricaSolo._key_list
        return midi_event

    @staticmethod
    def _increment_index():
        AfricaSolo._current_index = (AfricaSolo._current_index+1)&3

    @staticmethod
    def _generate_harmony_part(midi_event):
        if midi_event.type not in [NOTEON, NOTEOFF]:
            return midi_event
        if midi_event.note not in AfricaSolo._harmony_mapping.keys():
            return midi_event
        events = [midi_event]
        if AfricaSolo._harmony_part_on:
            note = AfricaSolo._harmony_mapping.get(midi_event.note,
                                             midi_event.note)
            midi_event2 = MidiEvent(
                midi_event.type,
                midi_event.port,
                midi_event.channel,
                note,
                midi_event.velocity)
            events.append(midi_event2)
        return events

    @staticmethod
    def _toggle_harmony_part():
        if set(AfricaSolo._key_list) == AfricaSolo._toggle_off_keys:
            AfricaSolo._harmony_part_on = False
        elif set(AfricaSolo._key_list) == AfricaSolo._toggle_on_keys:
            AfricaSolo._harmony_part_on = True

    @staticmethod
    def add_part(midi_event):
        AfricaSolo._register_key(midi_event)
        events = AfricaSolo._generate_harmony_part(midi_event)
        AfricaSolo._toggle_harmony_part()
        return events

def ResetAfricaSolo():
    return Process(AfricaSolo.reset)

def HarmonizeAfricaSolo():
    return Process(AfricaSolo.add_part)
