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
import time
import threading
from pyalsa.alsaseq import *
from subprocess import check_output
from constants import MIDIRIG_ALSA_CLIENT_NAME,MIDIRIG_DISPLAY_PORT
from mididings import SYSEX
from mididings.event import SysExEvent
from constants import DEFAULT_PORT

ARTURIA_ID = [0x00, 0x20, 0x6B]

def _append_space(st):
    l = 16 - len(st)
    for i in range(l):
        st = st + " "
    return st

def generate_name_msg(name):
    two_row_name = _split_into_two_rows(name)
    result = [0xf0] + ARTURIA_ID + [0x7F, 0x42, 0x04, 0x00, 0x60] 
    row_nr = 0x01
    for row in two_row_name:
        result.append(row_nr)
        row = _append_space(row)
        row = map(ord, row)
        result += row
        result.append(0x00)
        row_nr += 1
    result.append(0xf7)
    return result

def _split_into_two_rows(st):
    st = st.strip()
    if len(st) <= 16:
        return [st, ""]

    i = st[0:17].rfind(' ')
    if i == -1:
        return [st, ""]

    return [st[0:i].strip(), (st[i:].strip())[0:16]]

def generate_name_msg_as_str(name):
    bytes = generate_name_msg(name)
    return ' '.join('{:02x}'.format(x) for x in bytes)

def is_name_msg(midi_event):
    if midi_event.type == SYSEX:
        header = [0xf0] + ARTURIA_ID + [ 0x7F, 0x42, 0x04, 0x00, 0x60]
        for i, b in enumerate(header):
            if b != midi_event.sysex[i]:
                print "no match: {}!={}".format(b,
                    midi_event.sysex[i])
                return False
        return True
    else:
        return False

def generate_button_event(btn_nr, btn_value):
    btn_adr = 0x12 + btn_nr
    syx_msg = [
        0xF0,
        0x00,
        0x20,
        0x6B,
        0x7F,
        0x42,
        0x02,
        0x00,
        0x10,
        btn_adr,
        btn_value,
        0xF7]
    return SysExEvent(DEFAULT_PORT, syx_msg)

def generateToggledButtonEvents(btn_nr):
    event_list = []
    for i in range(10):
        btn_value = 127 * (i == btn_nr)
        syx_event = generate_button_event(i, btn_value)
        event_list.append( syx_event )
    return event_list


class ArturiaSysexTransmitter(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.stop_event = threading.Event()
        self._alsaseq = Sequencer(clientname=MIDIRIG_DISPLAY_PORT)
        if not self._alsaseq:
            print "Failed to create alsaseq.Sequenser()"
        self._port_id = -1
        self._port_id = self._alsaseq.create_simple_port(
            name = 'out',
            type = SEQ_PORT_TYPE_APPLICATION,
            caps = SEQ_PORT_CAP_SUBS_READ | \
                   SEQ_PORT_CAP_READ | \
                   SEQ_PORT_CAP_WRITE | \
                   SEQ_PORT_CAP_SUBS_WRITE)

        print "_port_id {}".format(self._port_id)
        self._midirig = None
        self._midirig_display = None
        self._connected = self.connect()
        self._print_connections()

    def run(self):
        while not self.stop_event.is_set():
            time.sleep(0.1)
            try:
                self._alsaseq.drain_output()
            except SequencerError:
                pass

    def _get_midirig_address(self):
        out = check_output(["aconnect", "-o"])
        i = out.find("MidiRigDisplay_in")
        if i > -1:
            i -= 4
            _port_id = out[i:(i + 3)].strip()
            i = out.find(MIDIRIG_ALSA_CLIENT_NAME)
            i -= 6
            client_id = out[i:(i + 3)].strip()
            return (int(client_id), int(_port_id))
        return None

    def _get_midirig_display_address(self):
        address = self._alsaseq.clientname + ":" + str(self._port_id)
        return self._alsaseq.parse_address(address)

    def send_text(self, text):
        syx = generate_name_msg(text)
        evt = self._create_event(syx)
        self._alsaseq.output_event(evt)

    def _create_event(self, sysexdata):
        event = SeqEvent(SEQ_EVENT_SYSEX, SEQ_TIME_STAMP_REAL)
        event.set_data({'ext': sysexdata})
        return event

    def connect(self):
        try:
            self._midirig_display = self._get_midirig_display_address()
            print "address: {}".format(self._midirig_display)
            self._midirig = self._get_midirig_address()
            if self._midirig:
                self._alsaseq.connect_ports(
                    self._midirig_display, self._midirig)
                print "Connection successful"
                return True
            else:
                print "MidiRig  not connected"
                return False
        except SequencerError as e:
            print "Could connect. {}".format(e.message)
            return False

    def stop(self):
        self.stop_event.set()

    def _print_connections(self):
        conlist = self._alsaseq.connection_list()
        for c in conlist:
            print "{}, ".format(c[0]),
            for p in c[2]:
                print "{}, ".format(p[0]),
                for cl in p[2]:
                    print "\t{}".format(cl)
