#!/bin/bash

PIN=23
echo $PIN > /sys/class/gpio/export
echo "out" > /sys/class/gpio/gpio$PIN/direction

function cleanup {
        echo "cleaning up"
        echo "0" > /sys/class/gpio/gpio$PIN/value
        echo $PIN > /sys/class/gpio/unexport
}
trap cleanup EXIT

connected_client=0
COUNTER=0
while true ; do
    if (( $connected_client == 0 )); then
	if (( $COUNTER % 2 == 0 )) ; then
	    echo "0" > /sys/class/gpio/gpio$PIN/value
        else
            echo "1" > /sys/class/gpio/gpio$PIN/value
	fi
    fi

    if (( $COUNTER % 4 == 0 )) ; then
        connected_client=`ping -c 1 -W 2 192.168.42.10 | grep "1 received" | wc -l`
	if (( $connected_client == 1 )); then
	    echo "1" > /sys/class/gpio/gpio$PIN/value
	fi
        COUNTER=0
    else
        sleep 1
    fi

    COUNTER=$(($COUNTER+1))
done
