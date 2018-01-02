#!/bin/bash
for service in `find /root/midirig/systemd_units/*.service -printf "%f\n" `; do
	echo $service
	systemctl is-failed $service
done 
