#!/bin/bash
#https://linuxize.com/cheatsheet/bash/
echo ========== SETUP ==========
repetitions=12345
nicelevel=-5
echo $repetitions repetitions
#evalcmd = python3 -c"from fileinput import input; print(sum(map(int, input()))/$repetitions)"
#alias evalcmd="awk '{sum+=$1; ssq+=$1^2} END {mean=sum/NR; sd=(ssq/NR - mean^2)^0.5; print \"Mean: \" mean \"\tStd Dev: \" sd}'"
#alias evalcmd
sudo renice $nicelevel $$
#chrt -p $$
#sudo chrt -r -p 70 $$
#chrt -p $$
echo ========== import ==========
for _ in $(seq 1 $repetitions)
do 
echo -n "$HOSTNAME",$nicelevel,"import", >> importoptim.csv
python3 << EOF >> importoptim.csv
import time
duration=-time.process_time_ns();
from importlib.util import find_spec
find_spec("typing")
duration+=time.process_time_ns();
print(duration)
EOF
done
echo ========== __import__ ==========
for _ in $(seq 1 $repetitions)
do 
echo -n "$HOSTNAME",$nicelevel,"__import__", >> importoptim.csv
python3 << EOF >> importoptim.csv
import time
duration=-time.process_time_ns();
__import__("importlib.util",globals(),locals(),fromlist=["util"]).find_spec("typing")
duration+=time.process_time_ns();
print(duration)
EOF
done
echo ========== __import__ + getattr ==========
for _ in $(seq 1 $repetitions)
do 
echo -n "$HOSTNAME",$nicelevel,"__import__ + getattr", >> importoptim.csv
python3 << EOF >> importoptim.csv
import time
duration=-time.process_time_ns();
getattr(__import__("importlib.util",globals(),locals(),fromlist=["util"]),"find_spec")("typing")
duration+=time.process_time_ns();
print(duration)
EOF
done
