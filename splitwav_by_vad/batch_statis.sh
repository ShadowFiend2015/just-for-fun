#!/bin/bash
# 用 test.py 脚本跑所有的被切割的音频，根据最后 1s 的分贝均值排序
result=()
for ((i = 9; i < 100; i += 10))
do
	for ((j = 9; j < 100; j += 10))
	do
		dir=origin-$i\_$j
		if [ ! -d "$dir" ]; then
			continue
		fi
		if [ `find $dir -type f | wc -l` -eq 1 ]
		then 
			rm -rf $dir
		else
			files=""
			for k in $( ls $dir)
			do
				files=${files}${dir}/$k" "
			done
			python test.py -f $files > ${dir}/static.log
			avg_db=`tail -n 1 ${dir}/static.log`
			result+=($avg_db---$dir)
		fi
	done
done
sorted=($(printf '%s\n' "${result[@]}"|sort))
for i in "${sorted[@]}"
do 
	echo $i
done
