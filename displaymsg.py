#!/usr/bin/python

import liblo
import sys
import conf

try:
    target = liblo.Address( conf.DISPLAY_OSC_ADDR )
except liblo.AddressError as err:
    print str(err)
    sys.exit()


args = len(sys.argv)
system_texts = {
        "--shutdown": conf.SHUTDOWN_MESSAGE,
        "--reboot": conf.REBOOT_MESSAGE,
        "--boot_complete": conf.BOOT_COMPLETE_MESSAGE,
        "--awaiting_device": conf.AWAITING_DEVICE_MESSAGE,
        "--system": sys.argv[2] if args > 2 else "No text",
        "--preview":sys.argv[2] if args > 2 else "No text"
        }

path = {"--preview":"/system/preview/text"}
system_path = "/system/msg"

if args < 2:
    osc_path = system_path
    msg = "No message"
else:
    arg = sys.argv[1]
    msg = system_texts.get( arg, "Unknown: {}".format( arg ))
    osc_path = path.get( arg, system_path)


#print "liblo.send(target, osc_path, msg)"
#print "liblo.send({}, {}, {})".format(conf.DISPLAY_OSC_ADDR, osc_path, msg)
try:
    liblo.send(target, osc_path, msg)
except BaseException:
    print("displaymsg: Unable to send OSCmessage ", sys.exc_info()[0])
