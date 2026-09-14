#!/bin/bash
sudo renice -20 $$
chrt -p $$
sudo chrt -r -p 70 $$
chrt -p $$
echo "====================================================================== TIMEIT ======================================================================"
echo "Importlib WALL"
python3 -OO -m timeit 'from importlib.util import find_spec; find_spec("typing")'
echo "Importlib PROCESS"
python3 -OO -m timeit --process 'from importlib.util import find_spec; find_spec("typing")'
echo "__import__ WALL"
python3 -OO -m timeit --process 'getattr(__import__("importlib.util",fromlist=[None]),"find_spec")("typing")'
echo "__import__ PROCESS"
python3 -OO -m timeit 'getattr(__import__("importlib.util",fromlist=[None]),"find_spec")("typing")'
echo "====================================================================== time ======================================================================"
echo "Importlib"
#time python3 -OO -c 'from importlib.util import find_spec; find_spec("typing")'
time for i in {1..100}; do python3 -OO -c 'from importlib.util import find_spec; find_spec("typing")'; done
echo "__import__"
#time python3 -OO -c 'getattr(__import__("importlib.util",fromlist=[None]),"find_spec")("typing")'
time for i in {1..100}; do python3 -OO -c 'getattr(__import__("importlib.util",fromlist=[None]),"find_spec")("typing")'; done
echo "====================================================================== importtime ======================================================================"
echo "Importlib"
python3 -OO -X importtime -c 'from importlib.util import find_spec; find_spec("typing")'
echo "__import__"
python3 -OO -X importtime -c 'getattr(__import__("importlib.util",fromlist=[None]),"find_spec")("typing")'
