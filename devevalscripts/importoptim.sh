#!/bin/bash
echo "====================================================================== SETUP ======================================================================"
sudo renice -20 $$
chrt -p $$
sudo chrt -r -p 70 $$
chrt -p $$
echo "====================================================================== TIMEIT ======================================================================"
echo "Importlib WALL"
python3 -OO -m timeit 'from importlib.util import find_spec; find_spec("typing")'
echo "__import__ WALL"
python3 -OO -m timeit '__import__("importlib.util",fromlist=["util"]).find_spec("typing")'
echo "__import__ WALL getattr"
python3 -OO -m timeit 'getattr(__import__("importlib.util",fromlist=["util"]),"find_spec")("typing")'
echo "Importlib PROCESS"
python3 -OO -m timeit --process 'from importlib.util import find_spec; find_spec("typing")'
echo "__import__ PROCESS"
python3 -OO -m timeit --process '__import__("importlib.util",fromlist=["util"]).find_spec("typing")'
echo "__import__ PROCESS getattr"
python3 -OO -m timeit --process 'getattr(__import__("importlib.util",fromlist=["util"]),"find_spec")("typing")'
echo "====================================================================== time ======================================================================"
echo "Importlib"
#time python3 -OO -c 'from importlib.util import find_spec; find_spec("typing")'
time for i in {1..50}; do python3 -OO -c 'from importlib.util import find_spec; find_spec("typing")'; done
echo "__import__"
time for i in {1..50}; do python3 -OO -c '__import__("importlib.util",fromlist=["util"]).find_spec("typing")'; done
echo "__import__ getattr"
#time python3 -OO -c 'getattr(__import__("importlib.util",fromlist=["util"]),"find_spec")("typing")'
time for i in {1..50}; do python3 -OO -c 'getattr(__import__("importlib.util",fromlist=["util"]),"find_spec")("typing")'; done
echo "====================================================================== importtime ======================================================================"
echo "Importlib"
python3 -OO -X importtime -c 'from importlib.util import find_spec; find_spec("typing")' 2>&1 | grep importlib\.util
echo "__import__ getattr"
python3 -OO -X importtime -c 'getattr(__import__("importlib.util",fromlist=["util"]),"find_spec")("typing")' 2>&1 | grep importlib\.util
echo "__import__"
python3 -OO -X importtime -c '__import__("importlib.util",fromlist=["util"]).find_spec("typing")' 2>&1 | grep importlib\.util
