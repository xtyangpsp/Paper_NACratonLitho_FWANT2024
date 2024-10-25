#!/bin/bash

list="dirs.list"
master="craton_station_withdata.txt"
outfile="craton_station_withdata_subset.txt"
cat /dev/null > $outfile
while read -r l
do
	net=`echo $l | awk '{print $1}'`
	sta=`echo $l | awk '{print $2}'`
	lon=`echo $l | awk '{print $3}'`
	lat=`echo $l | awk '{print $4}'`
	ele=`echo $l | awk '{print $5}'`
	netsta=`echo $net"."$sta`
	c=`grep $netsta $list | wc -c`
	if [ $c == 0 ]
		then
			echo $net $sta $lon $lat $ele >> $outfile
	fi
done < $master
