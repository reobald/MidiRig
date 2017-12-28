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
        self.originalLed = 0
        self.originalLcd = 0
        self.updated = 0
        self.previewing = False
        self.updateDisplay = display_cb

    def run(self):
        while not self.stop_event.is_set():
            if (self.previewing):
                now = time.time()
                passedTime = now - self.updated
                if(passedTime > 2):
                    self.updateDisplay(self.originalLed, self.originalLcd)
                    self.previewing = False
            time.sleep(2)

    def preview(self, origLed, origLcd, newLed, newLcd):
        self.originalLed = origLed
        self.originalLcd = origLcd
        self.updateDisplay(newLed, newLcd)
        self.previewing = True
        self.setTimeStamp()
#    def preview(self,browsed, original):
#	self.originalSound = original
#	self.updateDisplay(browsed);
#	self.browsing = True
#	self.setTimeStamp()

    def setTimeStamp(self):
        self.updated = time.time()

    def cancelPreview(self):
        self.previewing = False
