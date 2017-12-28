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

import RPi.GPIO as GPIO
import time
import threading


class BlinkingLed(threading.Thread):
    def __init__(self, pin):
        threading.Thread.__init__(self)

        self.pin = pin
        self.state = 0
        self.stop_event = threading.Event()

        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        GPIO.setup(self.pin, GPIO.OUT)
        GPIO.output(self.pin, 1)

    def run(self):
        while not self.stop_event.is_set():
            GPIO.output(self.pin, self.state)
            self.state = 0
            time.sleep(0.025)
        GPIO.cleanup()

    def blink(self):
        self.state = 1
