#!/bin/bash

PIN="24"
echo "$PIN" > /sys/class/gpio/export
echo "out" > /sys/class/gpio/gpio$PIN/direction

function cleanup {
        echo "cleaning up"
        echo "0" > /sys/class/gpio/gpio$PIN/value
        echo $PIN > /sys/class/gpio/unexport
}
trap cleanup EXIT

# Test for network conection
OnLine=0
while :
do
	if [[ $(cat /sys/class/net/wlan1/carrier) = 1 ]] ;  then
		if [ $OnLine = 0 ] ; then 
			OnLine=1 
			echo "Internet connection status: online"
			echo "1" > /sys/class/gpio/gpio$PIN/value
		fi
	else
		if [ $OnLine = 1 ] ; then
			OnLine=0
			echo  "Internet connection status: offline"
			echo "0" > /sys/class/gpio/gpio$PIN/value
		fi

	fi
	sleep 3
done
