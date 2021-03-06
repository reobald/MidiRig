#!/usr/bin/python
import sys
import RPi.GPIO as GPIO

# check for message i arguments
if len(sys.argv) < 2:
    print("ledcontroller: Wrong number of parameters")
    sys.exit()
else:
    channel = int(sys.argv[1])
    state = int(sys.argv[2])

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(channel, GPIO.OUT)


GPIO.output(channel, state)
