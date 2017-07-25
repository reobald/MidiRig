#! /bin/bash
for i in $(seq 55 $END); do 
	if (( $i<10 )); then
    		name="scene00$i.py"
	elif (( $i< 100 )); then
    		name="scene0$i.py"
	else
    		name="scene$i.py"
	fi
	cp template.py $name
done
