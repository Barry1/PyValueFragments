#!/bin/bash
echo ========== SETUP ==========
#sudo renice -20 $$
#chrt -p $$
#sudo chrt -r -p 70 $$
#chrt -p $$
repetitions=4
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
done
echo ========== __import__ ==========
for _ in $(seq 1 $repetitions)
do python3 << EOF
import time
duration=-time.process_time_ns();
__import__("importlib.util",globals(),locals(),fromlist=["util"]).find_spec("typing")
duration+=time.process_time_ns();
print(duration)
EOF
done
echo ========== __import__ + getattr ==========
for _ in $(seq 1 $repetitions)
do python3 << EOF
import time
duration=-time.process_time_ns();
getattr(__import__("importlib.util",globals(),locals(),fromlist=["util"]),"find_spec")("typing")
duration+=time.process_time_ns();
print(duration)
EOF
done
