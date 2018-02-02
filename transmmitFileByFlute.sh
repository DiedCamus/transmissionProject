#!/bin/bash
flutepath=/home/ofcl/Documents/sender/unicast_sender/mad_fcl_v1.7_src/bin/flute
sip1=192.168.1.10
rip1=192.169.1.13
sip2=192.168.2.10
rip2=192.168.2.12
filepath=/home/ofcl/Downloads/
#savepath=/home/hualong2/Documents/hualong/server/saveFiles/
flute1="$flutepath -S -k:2 -m:192.168.1.10 -p:4000 -t:2 -i:192.168.1.13 -r:5000000 -n:1 -F:"
flute2="$flutepath -S -k:2 -m:192.168.2.10 -p:4001 -t:2 -i:192.168.2.12 -r:5000000 -n:1 -F:"
gaptime=$1
filenumber=$2
is_sent=true
count=0
count1=0
count2=0
filename1="dataforhttp_one"
filename1_full=${filename1}"0.data"
filename2="dataforhttp_two"
filename2_full=${filename2}"0.data"

sendfile(){
	ison_flute1=`ps -ef|grep $sip1|grep -v grep|awk '{print $2}'`
	if [ -n $ison_flute1 ]; then
		echo "use flute1"
		mv ${filepath}${filename1_full} ${filepath}${filename1}${count1}".data"
		filename1_full=${filename1}${count1}".data"
		${flute1}${filepath}${filename1_full} &
		sleep 1
		let count1++
		#mv ${filepath}$filename_full ${filepath}${filename}${count}".data"
		is_sent=true
		return
	else
		echo "flute1 is in use"
		ison_flute2=`ps -ef|grep $sip2|grep -v grep|awk '{print $2}'`
		if [ -n $ison_flute2 ]; then
			echo "use flute2"
			mv ${filepath}${filename2_full} ${filepath}${filename2}${count2}".data"
			filename_full2=${filename2}${count2}".data"
			${flute2}${filename2_full} &
			sleep 1
			let count2++
			is_sent=true
			return
		fi
	fi
	echo "all flutes are in use"
	is_sent=false
}

sendfile_flute1(){
	ison_flute1=`ps -ef|grep $sip1 |grep -v grep|awk '{print $2}'`
	#echo "ison_flute1 = ${ison_flute1}"
	if [ -n $ison_flute1 ]; then
		mv ${filepath}${filename_full} ${filepath}${filename}${count}".data"
		filename_full=${filename}${count}".data"
		echo "ison_flute1 is NULL, flute is not on"
		${flute1}${filepath}${filename_full} &
		sleep 1
		let count++
		#mv ${filepath}${filename_full} ${filepath}${filename}${count}".data"
		echo "conut=$count, $filename_full is sent"
		#mv ${filepath}${filename_full} ${filepath}${filename}${count}".data"
	else
		echo "flute1 is in using"
	fi
}

sendfile_flute2(){
        ison_flute2=`ps -ef|grep $sip2 |grep -v grep|awk '{print $2}'`
        #echo "ison_flute1 = ${ison_flute1}"
        if [ -n $ison_flute2 ]; then
                mv ${filepath}${filename_full} ${filepath}${filename}${count}".data"
                filename_full=${filename}${count}".data"
                echo "ison_flute2 is NULL, flute is not on"
                ${flute2}${filepath}${filename_full} &
                sleep 1
                let count++
                #mv ${filepath}${filename_full} ${filepath}${filename}${count}".data"
                echo "conut=$count, $filename_full is sent"
                #mv ${filepath}${filename_full} ${filepath}${filename}${count}".data"
        else
                echo "flute2 is in using"
        fi
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
	count1=0
	count2=0
	count=`expr $count1 + $count2`
	while [ $count -lt $filenumber ]
	do
		#count=`expr $count1 + $count2`
		#filename_full=${filename}${count}".data"
		#sendfile_flute1
		sendfile
		count=`expr $count1 + $count2`
		#if ${is_sent}; then
		#	echo "success"
		#else
		#	echo "failed"
		#fi
			
	done
	#filename_full=${filename}${count}".data"
	mv ${filepath}${filename1_full} ${filepath}${filename1}"0.data"
	mv ${filepath}${filename2_full} ${filepath}${filename2}"0.data"
	echo "one turn end"
sleep $gaptime
done
