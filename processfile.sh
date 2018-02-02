#!/bin/bash
tube_number=$1
flutepath=/home/ofcl/Documents/sender/unicast_sender/mad_fcl_v1.7_src/bin/flute
sip1=192.168.1.10
rip1=192.169.1.13
sip2=192.168.2.10
rip2=192.168.2.12
filepath=/home/ofcl/Documents/hualong/transmissionProject/uploadServer/uploadFiles/
#savepath=/home/hualong2/Documents/hualong/server/saveFiles/
flute1="$flutepath -S -k:2 -m:192.168.1.10 -p:4000 -t:2 -i:192.168.1.13 -r:5000000 -n:1 -F:"
flute2="$flutepath -S -k:2 -m:192.168.2.10 -p:4000 -t:2 -i:192.168.2.12 -r:5000000 -n:1 -F:"

function send_withflute1(){
	if [ "$(ls -A $filepath)" ]; then
		allfiles=$(find $filepath -type f)
		for entry in $allfiles
		do
		if [ "${entry##*.}" != "sent" ]; then
			#echo "file: $entry has been sent"
			echo "new file: $entry"
			ison_flute1=`ps -ef|grep $sip1|grep -v grep|awk '{print $2}'`
			if [ -n $ison_flute1 ]; then
			#($flutepath -S -m:192.168.1.10 -p:4000 -t:2 -i:192.168.1.13 -r:5000000 -n:1 -F:$entry)&&(mv $entry $entry.sent) &	
			#$flutepath -S -m:${sip1} -p:4000 -t:2 -i:${rip1} -r:5000000 -n:1 -F:${entry} &&(mv $entry $entry.sent) &
			(${flute1}${entry})&&(mv $entry $entry.sent) &
		fi
		done
	fi

}

function send_withflute2(){
	if [ "$(ls -A $filepath)" ]; then
		allfiles=$(find $filepath -type f)
		for entry in $allfiles
		do
		if [ "${entry##*.}" != "sent" ]; then
			#echo "file: $entry has been sent"
			echo "new file: $entry"
			ison_flute2=`ps -ef|grep $sip2|grep -v grep|awk '{print $2}'`
			if [ -n $ison_flute2 ]; then
			#($flutepath -S -m:192.168.1.10 -p:4000 -t:2 -i:192.168.1.13 -r:5000000 -n:1 -F:$entry)&&(mv $entry $entry.sent) &	
			#$flutepath -S -m:${sip1} -p:4000 -t:2 -i:${rip1} -r:5000000 -n:1 -F:${entry} &&(mv $entry $entry.sent) &
			(${flute2}${entry})&&(mv $entry $entry.sent) &
		fi
		done
	fi

}

function send_withbothflute(){
	if [ "$(ls -A $filepath)" ]; then
		allfiles=$(find $filepath -type f)
		for entry in $allfiles
		do
		if [ "${entry##*.}" != "sent" ]; then
			#echo "file: $entry has been sent"
			echo "new file: $entry"
			ison_flute1=`ps -ef|grep $sip1|grep -v grep|awk '{print $2}'`
			if [ -n $ison_flute1 ]; then
			#($flutepath -S -m:192.168.1.10 -p:4000 -t:2 -i:192.168.1.13 -r:5000000 -n:1 -F:$entry)&&(mv $entry $entry.sent) &	
			#$flutepath -S -m:${sip1} -p:4000 -t:2 -i:${rip1} -r:5000000 -n:1 -F:${entry} &&(mv $entry $entry.sent) &
			(${flute1}${entry})&&(mv $entry $entry.sent) &
			else
				ison_flute2=`ps -ef|grep $sip2|grep -v grep|awk '{print $2}'`
				if [ -n $ison_flute2 ]; then
					#($flute -S -m:$sip2 -p:4000 -t:2 -i:$rip2 -r:5000000 -n:1 -F:$entry)&&(mv $entry $entry.sent) &
					(${flute2}${entry})&&(mv $entry $entry.sent) &
				fi
			fi
               #$flute -S -m:192.168.1.10 -p:4000 -t:2 -i:192.168.1.13 -r:5000000 -n:1 -F:$entry
               #mv $entry $entry.sent
		fi
		done
	fi

}

while [ 1 ]
do
	case tube_number in
		1)
		echo "use flute1"
		send_withflute1
		;;
		2)
		echo "use flute2"
		send_withflute2
		;;
		0)
		echo "use both flutes"
		send_withbothflute
		;;
		*)
		echo "help: [ 0|use both flutes ] [ 1|use flute1 ] [ 2|use flute2 ]"
		exit
		;;
	esac

sleep 1
done
