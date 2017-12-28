#!/usr/bin/python

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

import liblo
import sys
import smbus
import time
import signal
import threading
import subprocess
from previewer import Previewer
from arturia_sysex import ArturiaSysexTransmitter

# mididings global variables
data_offset = 0
scenes = {}
tmp_scenes = {}
current_scene = 0

# I2C
i2cbus = smbus.SMBus(1)
i2caddress = 0x04

# Midirig display commands
UPDATE_SEVEN_SEG_NUMBER = 0
UPDATE_LCD_ROW1 = 1
UPDATE_LCD_ROW2 = 2
CLEAR_LCD = 3
UPDATE_SEVEN_SEG_TEXT = 4

ACK = 0
ERR = 1

# constants
ROW1 = 0
ROW2 = 1
ALL = 2

# Arturia display
sysex_trx = ArturiaSysexTransmitter()
sysex_trx.start()


def update_arturia_display(lcd_text):
    sysex_trx.send_text(lcd_text)


def i2c_write_string(cmd, str):
    datalist = map(ord, str)
    i2cbus.write_i2c_block_data(i2caddress, cmd, datalist)
    print("Raspberry pi: {0}, {1}, {2}".format(i2caddress, cmd, datalist))


def i2c_write_byte(cmd, value):
    i2cbus.write_byte_data(i2caddress, cmd, value)
    print("Raspberry pi: {0}, {1}, {2}".format(i2caddress, cmd, value))


def i2c_write_bytes(cmd, bytes):
    i2cbus.write_i2c_block_data(i2caddress, cmd, bytes)
    print("Raspberry pi: {0}, {1}, {2}".format(i2caddress, cmd, bytes))


def to_bytes(input):
    byte1 = input & 255
    byte2 = input >> 8
    return [byte1, byte2]


def i2c_wait_for_ack():
    for i in range(100):
        time.sleep(0.001)
        result = i2cbus.read_byte(i2caddress)
        if result == ACK:
            print("Arduino     : ACK")
            return True
        if result == ERR:
            print("Arduino     : ERR")
            return False
    print("Arduino     : Timeout")
    return False


def split_into_two_rows(st):
    st = st.strip()
    if len(st) <= 16:
        return [st, ""]

    i = st[0:17].rfind(' ')
    if i == -1:
        return [st, ""]

    return [st[0:i].strip(), st[i:].strip()]


def get_scene_name(scene_number):
    global scenes
    try:
        scene_info = scenes[scene_number]
        name = scene_info[0]
    except KeyError:
        name = "Unknown"
    return name


def update_7seg_number(scene_number):
    bytes = to_bytes(scene_number)
    i2c_write_bytes(UPDATE_SEVEN_SEG_NUMBER, bytes)
    if not i2c_wait_for_ack():
        return


def update_7seg_text(txt):
    i2c_write_string(UPDATE_SEVEN_SEG_TEXT, txt)
    if not i2c_wait_for_ack():
        return


def update_display_msg(input_text):
    divided_text = split_into_two_rows(input_text)

    i2c_write_byte(CLEAR_LCD, ALL)
    if not i2c_wait_for_ack():
        return
    i2c_write_string(UPDATE_LCD_ROW1, divided_text[ROW1])
    if not i2c_wait_for_ack():
        return
    i2c_write_string(UPDATE_LCD_ROW2, divided_text[ROW2])
    if not i2c_wait_for_ack():
        return


lock = threading.Lock()


def update_display(sevseg_info, lcd_text):
    print "update_display: {}".format(lcd_text)
    try:
        lock.acquire()
        try:
            update_7seg_number(sevseg_info)
            arturia_msg = "{}: {}".format(sevseg_info, lcd_text)
        except TypeError:
            update_7seg_text(sevseg_info)
            arturia_msg = "{}".format(lcd_text)
        update_display_msg(lcd_text)
        update_arturia_display(arturia_msg)
    finally:
        lock.release()


# create server, listening on port 56419
try:
    server = liblo.Server(56419)
except liblo.ServerError as err:
    print(err)
    sys.exit()

previewer = Previewer(update_display)
previewer.start()

# create handler for graceful exit


def handler(signum, frame):
    previewer.stop_event.set()
    sysex_trx.stop()
    print 'Exiting midirig_display'
    sys.exit()


# attach handler to system signals
signal.signal(signal.SIGTERM, handler)
signal.signal(signal.SIGINT, handler)

#('/mididings/data_offset', 'i')


def data_offset_cb(path, args):
    global data_offset
    data_offset = args[0]
    print(path, args)


server.add_method("/mididings/data_offset", 'i', data_offset_cb)


#('/mididings/begin_scenes', '')
def begin_scenes_cb(path, args):
    global tmp_scenes
    tmp_scenes = {}
    print(path, args)


server.add_method("/mididings/begin_scenes", '', begin_scenes_cb)

#('/mididings/add_scene', None)


def add_scene_cb(path, args):
    global tmp_scenes
    number, name = args[:2]
    print(number)
    subscenes = args[2:]
    tmp_scenes[number] = (name, subscenes)
    print(path, args)


server.add_method("/mididings/add_scene", None, add_scene_cb)

#('/mididings/end_scenes', '')


def end_scenes_cb(path, args):
    global scenes
    global tmp_scenes
    scenes = tmp_scenes
    print(path, args)


server.add_method("/mididings/end_scenes", '', end_scenes_cb)

#('/mididings/current_scene', 'ii')


def current_scene_cb(path, args):
    previewer.cancel_preview()
    global current_scene
    current_scene = args[0]
    scene_name = get_scene_name(current_scene)
    update_display(current_scene, scene_name)
    print(path, args)


server.add_method("/mididings/current_scene", 'ii', current_scene_cb)

#('/system/preview/scene', 'i')


def system_preview_scene_cb(path, args):
    print(path, args)
    preview_led = args[0]
    preview_lcd = get_scene_name(preview_led)
    orig_led = current_scene
    orig_lcd = get_scene_name(current_scene)
    previewer.preview(orig_led, orig_lcd, preview_led, preview_lcd)


server.add_method("/system/preview/scene", 'i', system_preview_scene_cb)

#('/system/preview/text', 's')


def system_preview_text_cb(path, args):
    print(path, args)
    preview_led = "   "
    preview_lcd = args[0]
    orig_led = current_scene
    orig_lcd = get_scene_name(current_scene)
    previewer.preview(orig_led, orig_lcd, preview_led, preview_lcd)


server.add_method("/system/preview/text", 's', system_preview_text_cb)

#('/system/msg', 's')


def system_msg_cb(path, args):
    update_display("---", args[0])
    print(path, args)


server.add_method("/system/msg", 's', system_msg_cb)


# Fallback method
def fallback(path, args, types, src):
    print("got unknown message '%s' from '%s'" % (path, src.url))
    for a, t in zip(args, types):
        print("argument of type '%s': %s" % (t, a))


server.add_method(None, None, fallback)


# loop and dispatch messages every 100ms
print("Server listening at port 56419")
while True:
    server.recv(100)
