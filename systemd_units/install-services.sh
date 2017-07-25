#!/bin/bash

#####################
# hostapd_indicator #
#####################
systemctl enable `pwd`/hostapd_indicator.service

############################
# network_online_indicator #
############################
systemctl enable `pwd`/network_online_indicator.service

###################
# midirig_display #
###################
systemctl enable `pwd`/midirig_display.service

##################
# shutdownbutton #
##################
systemctl enable `pwd`/shutdownbutton.service

###########
# midirig #
###########
#first override sound.target parameter, so that midirig is started after.
#make a new directory as a container for the overriding configuration
mkdir -p /etc/systemd/system/sound.target.d
#copy the file containing the overriding configuration
cp -rf ./sound.target.d/midirig_override.config /etc/systemd/system/sound.target.d
#enable the service
systemctl enable `pwd`/midirig.service
