from subprocess import check_output
import sys
print __file__
#def getMidiPort(name):
#   midiports = {}
#   out = check_output(["aplaymidi", "-l"])
#   for line in out.splitlines():
#      port =  line[:9].strip()
#      client= line[9:42].strip()
#      midiports[client]=port
#   return midiports[name]
#
#try:
#	dest_port = getMidiPort("KeyLab 61")#
#	print dest_port
#	ev = _mididings.MidiEvent()
#	ev.type_ = getattr(_mididings.MidiEventType, "SYSEX")
#	ev.port_ = 0
#
#	sysex = "F0 00 20 6B 7F 42 04 00  60 01 50 72 65 73 65 74 20 6C 6F 61 64 65 64 3A  00 02 32 50 6F 6C 65 20 41 6E 61 6C 6F 67 20 42  72 61 00 F7".split()
#	ev.sysex_ = bytearray(int(x, 16) for x in sysex)
#	_mididings.send_midi('alsa', dest_port, ev)
#except Exception as ex:
#   	sys.exit("send_midi: error: %s" % ex)
