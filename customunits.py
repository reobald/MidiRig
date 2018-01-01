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

from mididings import *
from mididings.extra.osc import SendOSC
from mididings.extra.gm import *
from constants import INTEGRA7_PORT

####################
# Global variables
####################
group = {'STUDIO SET': [85, 0],  # Studio set
         'SN-A USER': [89, 0],  # User SN AcousticTone
         'SN-A PRST': [89, 64],  # Preset SNA cousticTone
         'SN-S USER': [95, 0],  # User SN SynthTone
         'SN-S PRST': [95, 64],  # Preset SN SynthTone
         'SN-D USER': [88, 0],  # User SN DrumKit
         'SN-D PRST': [88, 64],  # Preset SN DrumKit
         'PCMS USER': [87, 0],  # User PCM SynthTone
         'PCMS PRST': [87, 64],  # Preset PCM SynthTone
         'PCMS GM2': [121, 0],  # GM2 Tone
         'PCMD USER': [86, 0],  # User PCM DrumKit
         'PCMD PRST': [86, 64],  # Preset PCM DrumKit
         'PCMD GM2': [120, 0],  # GM2 DrumKit
         'PCMS SRX01': [93, 0],  # Expansion PCM Tone (SRX01)
         'PCMD SRX01': [92, 0],  # Expansion PCM Drum (SRX01)
         'PCMS SRX02': [93, 1],  # Expansion PCM Tone (SRX02)
         'PCMS SRX03': [93, 2],  # Expansion PCM Tone (SRX03)
         'PCMD SRX03': [92, 2],  # Expansion PCM Drum (SRX03)
         'PCMS SRX04': [93, 3],  # Expansion PCM Tone (SRX04)
         'PCMS SRX05': [93, 4],  # Expansion PCM Tone (SRX05)
         'PCMD SRX05': [92, 4],  # Expansion PCM Drum (SRX05)
         'PCMS SRX06': [93, 7],  # Expansion PCM Tone (SRX06)
         'PCMD SRX06': [92, 7],  # Expansion PCM Drum (SRX06)
         'PCMS SRX07': [93, 11],  # Expansion PCM Tone (SRX07)
         'PCMD SRX07': [92, 11],  # Expansion PCM Drum (SRX07)
         'PCMS SRX08': [93, 15],  # Expansion PCM Tone (SRX08)
         'PCMD SRX08': [92, 15],  # Expansion PCM Drum (SRX08)
         'PCMS SRX09': [93, 19],  # Expansion PCM Tone (SRX09)
         'PCMD SRX09': [92, 19],  # Expansion PCM Drum (SRX09)
         'PCMS SRX10': [93, 23],  # Expansion PCM Tone (SRX10)
         'PCMS SRX11': [93, 24],  # Expansion PCM Tone (SRX11)
         'PCMS SRX12': [93, 26],  # Expansion PCM Tone (SRX12)
         'SN-A ExSN1': [89, 96],  # Expansion SN Tone (ExSN1)
         'SN-A ExSN2': [89, 97],  # Expansion SN Tone (ExSN2)
         'SN-A ExSN3': [89, 98],  # Expansion SN Tone (ExSN3)
         'SN-A ExSN4': [89, 99],  # Expansion SN Tone (ExSN4)
         'SN-A ExSN5': [89, 100],  # Expansion SN Tone (ExSN5)
         'SN-A ExSN6': [89, 101],  # Expansion SN Tone (ExSN6)
         'PCMS ExPCM': [97, 0],  # Expansion PCM Tone (ExPCM)
         'PCMS ExPCM': [96, 0],  # Expansion PCM Drum (ExPCM)
         'PCMS GM2#': [121, 0],  # Expansion GM2 Tone (GM2#)
         'PCMD GM2#': [120, 0],  # Expansion GM2 Drum (GM2#)
         'NORD ELECTRO': [0, 0]  # Nord Electro 2
         }
INDEX_GROUPNR = 0
INDEX_LSBOFFSET = 1
transposeOffset = 0


####################
# Helper functions
####################

def convertToPgcInfo(groupname, nr):
    nr = nr - 1
    msb = group[groupname][INDEX_GROUPNR]
    lsbOffset = group[groupname][INDEX_LSBOFFSET]
    lsb = (nr >> 7) & (0x7f)
    lsb = lsb + lsbOffset
    nr = nr & 0x7f
    nr = nr + 1
    return {'msb': msb, 'lsb': lsb, 'nr': nr}


def transposeUp(midievent):
    global transposeOffset
    transposeOffset += 1
    print "transpose up:" + str(transposeOffset)
    return midievent


def transposeDown(midievent):
    global transposeOffset
    transposeOffset -= 1
    print "transpose down:" + str(transposeOffset)
    return midievent


def transposeReset(midievent):
    global transposeOffset
    transposeOffset = 0
    return midievent


def getTransposeMsg(midievent):
    text = "**** EDIT **** "
    text += "Transpose: "
    text += str(transposeOffset)
    return text


def globalTranspose(midievent):
    try:
        midievent.note += transposeOffset
        return midievent
    except BaseException:
        return midievent


######################
# Mididings extensions
######################

# Sends bank select and program change messages
def ProgramChange(ch, group, nr, port=INTEGRA7_PORT):
    pgcInfo = convertToPgcInfo(group, nr)
    pgChange = Program(port, ch, pgcInfo['nr'])
    bankSelMsb = Ctrl(port, ch, 0x00, pgcInfo['msb'])
    bSelLsb = Ctrl(port, ch, 0x20, pgcInfo['lsb'])
    return [bankSelMsb, bSelLsb, pgChange]

# Converts a cc11 expression message on a certain midi channel to an new
# controller


def ConvertExpression(ch, cc):
    return ChannelFilter(ch) % CtrlMap(CTRL_EXPRESSION, cc)

# connects sustain pedal messages for two channels


def ConnectSusPedals(chA, chB):
    return (ChannelFilter(chA) & CtrlFilter(
        CTRL_SUSTAIN)) % [Pass(), Channel(chB)]


def SetGlobalTranspose():
    return CtrlFilter(79) % (((CtrlValueFilter(64) % Process(transposeReset)) >> (
        CtrlValueFilter(0) % Process(transposeDown)) >> (
        CtrlValueFilter(127) % Process(transposeUp))) >> SendOSC(
            56419,
            "/system/preview/text",
        getTransposeMsg))


def CC82toCH16():
    return CtrlFilter(82) % Channel(16)


def GlobalTranspose():
    return Process(globalTranspose)
