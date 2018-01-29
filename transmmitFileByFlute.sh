#!/bin/bash
flutepath=/home/ofcl/Documents/sender/unicast_sender/mad_fcl_v1.7_src/bin/flute
sip1=192.168.1.10
rip1=192.169.1.13
sip2=192.168.2.10
rip2=192.168.2.13
filepath=/home/ofcl/Documents/hualong/server/uploadFiles/
#savepath=/home/hualong2/Documents/hualong/server/saveFiles/
flute1="$flutepath -S -m:192.168.1.10 -p:4000 -t:2 -i:192.168.1.13 -r:5000000 -n:1 -F:"
flute2="$flutepath -S -m:192.168.2.10 -p:4000 -t:2 -i:192.168.2.13 -r:5000000 -n:1 -F:"
gaptime=$1
filenumber=$2
is_sent=true
count=0
filename="datafile"
filename_full=${filename}"0.data"

sendfile(){
	ison_flute1=`ps -ef|grep $sip1|grep -v grep|awk '{print $2}'`
	if [ -n $ison-flute1 ]; then
		echo "use flute1"
		(${flute1}${filename_full})&&(let count++)&&(mv $filename_full ${filename}${count}".data") &
		is_sent=true
		return
	else
		echo "flute1 is in use"
		ison_flute2=`ps -ef|grep $sip2|grep -v grep|awk '{print $2}'`
		if [ -n $sip2 ]; then
			echo "use flute2"
			${flute2}${filename_full} &
			is_sent=true
			return
		fi
	fi
	echo "all flutes are in use"
	is_sent=false
}

#for function test
cpfile(){
	cp /home/hualong/Desktop/file1/${filename_full} /home/hualong/Desktop/file2/
	let count++
	echo $count
	mv /home/hualong/Desktop/file1/${filename_full} /home/hualong/Desktop/file1/${filename}${count}".data"
	is_sent=true
}

while true
do
	count=0
	while [ $count -lt $filenumber ]
	do
		filename_full=${filename}${count}".data"
		cpfile
		if ${is_sent}; then
			echo "success"
		else
			echo "failed"
		fi
			
	done
	filename_full=${filename}${count}".data"
	mv /home/hualong/Desktop/file1/${filename_full} /home/hualong/Desktop/file1/${filename}"0.data"
	echo "one turn end"
sleep $gaptime
done
