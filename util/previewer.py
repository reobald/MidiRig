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


class Previewer(threading.Thread):
    def __init__(self, display_cb):
        threading.Thread.__init__(self)
        self.stop_event = threading.Event()
        self.original_led = 0
        self.original_lcd = 0
        self.updated = 0
        self.previewing = False
        self.update_display = display_cb

    def run(self):
        while not self.stop_event.is_set():
            if (self.previewing):
                now = time.time()
                passed_time = now - self.updated
                if(passed_time > 2):
                    self.update_display(self.original_led, self.original_lcd)
                    self.previewing = False
            time.sleep(2)

    def preview(self, orig_led, orig_lcd, new_led, new_lcd):
        self.original_led = orig_led
        self.original_lcd = orig_lcd
        self.update_display(new_led, new_lcd)
        self.previewing = True
        self._set_time_stamp()

    def _set_time_stamp(self):
        self.updated = time.time()

    def cancel_preview(self):
        self.previewing = False
