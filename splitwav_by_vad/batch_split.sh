#!/bin/bash
# according to both vad_prob_start and vad_prob_continue added from 9 to 99 step by 10, slices the wav 10*10=100 times.
file="origin"
filetype=".wav"

for ((i = 9; i < 100; i += 10))
do
	for ((j = 9; j < 100; j += 10))
	do
		./splitwav -config vad.toml -f $file$filetype -vps $i -vpc $j 2>logs/$i-$j-err.log 1>logs/$i-$j-std.log &
	done
done
