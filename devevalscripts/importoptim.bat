@echo off
rem pushd \\wsl.localhost\Debian\home\ebeling\GitHub\PyValueFragments\devevalscripts
rem net use W: \\wsl.localhost\Debian
set repetitions=1234
echo ====================================================================== timeit WALL ======================================================================
echo Importlib
python3 -OO -m timeit --number %repetitions% "from importlib.util import find_spec; find_spec(""typing"")"
echo __import__ getattr
python3 -OO -m timeit --number %repetitions% "getattr(__import__(""importlib.util"",fromlist=[""util""]),""find_spec"")(""typing"")"
echo __import__
python3 -OO -m timeit --number %repetitions% "__import__(""importlib.util"",fromlist=[""util""]).find_spec(""typing"")"
echo ====================================================================== timeit PROCESS ======================================================================
echo Importlib process
python3 -OO -m timeit --process --number %repetitions% "from importlib.util import find_spec; find_spec(""typing"")"
echo __import__ getattr process
python3 -OO -m timeit --process --number %repetitions% "getattr(__import__(""importlib.util"",fromlist=[""util""]),""find_spec"")(""typing"")"
echo __import__ process
python3 -OO -m timeit --process --number %repetitions% "__import__(""importlib.util"",fromlist=[""util""]).find_spec(""typing"")"
echo ====================================================================== importtime ======================================================================
rem python3 -OO -X importtime -c "from importlib.util import find_spec; find_spec(""typing"")" 
rem python3 -OO -X importtime -c "getattr(__import__(""importlib.util"",fromlist=[""util""]),""find_spec"")(""typing"")" 
rem python3 -OO -X importtime -c "__import__(""importlib.util"",fromlist=[""util""]).find_spec(""typing"")" 
