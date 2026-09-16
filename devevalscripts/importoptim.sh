#!/bin/bash
echo ========== SETUP ==========
repetitions=12345
echo $repetitions repetitions
#evalcmd = python3 -c"from fileinput import input; print(sum(map(int, input()))/$repetitions)"
#evalcmd="awk '{sum+=$1; ssq+=$1^2} END {mean=sum/NR; sd=(ssq/NR - mean^2)^0.5; print \"Mean: \" mean \"\tStd Dev: \" sd}'"
#echo $evalcmd
#sudo renice -18 $$
#chrt -p $$
#sudo chrt -r -p 70 $$
#chrt -p $$
echo ========== import ==========
for _ in $(seq 1 $repetitions)
do python3 << EOF
import time
duration=-time.process_time_ns();
from importlib.util import find_spec
find_spec("typing")
duration+=time.process_time_ns();
print(duration)
EOF
done | awk '{sum+=$1; ssq+=$1^2} END {mean=sum/NR; sd=(ssq/NR - mean^2)^0.5; print "Mean: " mean "\tStd Dev: " sd}'
echo ========== __import__ ==========
for _ in $(seq 1 $repetitions)
do python3 << EOF
import time
duration=-time.process_time_ns();
__import__("importlib.util",globals(),locals(),fromlist=["util"]).find_spec("typing")
duration+=time.process_time_ns();
print(duration)
EOF
done | awk '{sum+=$1; ssq+=$1^2} END {mean=sum/NR; sd=(ssq/NR - mean^2)^0.5; print "Mean: " mean "\tStd Dev: " sd}'
echo ========== __import__ + getattr ==========
for _ in $(seq 1 $repetitions)
do python3 << EOF
import time
duration=-time.process_time_ns();
getattr(__import__("importlib.util",globals(),locals(),fromlist=["util"]),"find_spec")("typing")
duration+=time.process_time_ns();
print(duration)
EOF
done | awk '{sum+=$1; ssq+=$1^2} END {mean=sum/NR; sd=(ssq/NR - mean^2)^0.5; print "Mean: " mean "\tStd Dev: " sd}'
#========== SETUP ==========
# 1234
#========== import ==========
#Mean: 1.45871e+06	Std Dev: 108186
#========== __import__ ==========
#Mean: 1.46049e+06	Std Dev: 114741
#========== __import__ + getattr ==========
#Mean: 1.46202e+06	Std Dev: 117371
#
#real	7m5,676s
#user	3m56,485s
#sys	3m27,012s

#========== SETUP ==========
#12345 repetitions
#========== import ==========
#Mean: 1.46436e+06	Std Dev: 112609
#========== __import__ ==========
#Mean: 1.46568e+06	Std Dev: 90738.9
#========== __import__ + getattr ==========
#Mean: 1.4637e+06	Std Dev: 94193.5
#2366.60user 2152.96system 1:12:05elapsed 104%CPU (0avgtext+0avgdata 9888maxresident)k
#0inputs+32outputs (52major+637798600minor)pagefaults 0swaps
