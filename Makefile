.PHONY = default build buildprep install pyre pyreanalyse pyrecheck pyreinfer pytype prospector sourcery
#should max-load be num-cpus?
MAKEFLAGS += --jobs --max-load=2 --output-sync=target
#https://www.gnu.org/software/make/manual/html_node/Wildcard-Function.html
#PYOBJS = $(wildcard *.py)
#pyobjs:= $(shell tree -if | egrep .pyi?$$)
#pyobjs:= $(shell find src -regex .*pyi?$$)
pyobjs!= find src -regex .*\.pyi?$$

pyrefly:
	poetry run pyrefly check

sourcery:
	poetry run sourcery review src/valuefragments --fix --summary --verbose

flynt:
	poetry run flynt src/valuefragments

trunkchkfmt:
	trunk check src/valuefragments

actsuperlinter:
	act --graph
	act --job run-lint

typings/joblib/joblib/externals/loky/process_executor.pyi:
	poetry run pyright src/valuefragments/contextmanagers.py --createstub joblib.externals.loky.process_executor

typings/joblib/joblib/externals/loky/reusable_executor.pyi:
	poetry run pyright src/valuefragments/contextmanagers.py --createstub joblib.externals.loky.reusable_executor 

typings/cpu_load_generator/_interface.pyi:
	poetry run pyright src/valuefragments/contextmanagers.py --createstub cpu_load_generator

stubs:
	poetry run pyright --createstub joblib
	poetry run pyright --createstub icecream
	poetry run pyright --createstub valuefragments
	poetry run pyright --createstub cpu_load_generator
	poetry run pyright --createstub hashlib
	poetry run pyright --createstub psutil

default: formatters pylint pydocstyle pyright checkminver

trunk:
	poetry run trunk check --all

pyanalyze:
	poetry run python -m pyanalyze src/valuefragments

mypy:
	poetry run mypy --strict --show-error-codes src/valuefragments/

prospector:
	poetry run prospector src

checkminver:
	poetry run vermin --target=3.12- --lint -vv --eval-annotations --no-parse-comments --backport asyncio --backport typing --backport typing_extensions src

formatters:
#	@echo "==========" "autopep8" "=========="
#	poetry run autopep8 $(pyobjs)
	@echo "==========" "isort" "=========="
	poetry run isort $(pyobjs)
	@echo "==========" "black" "=========="
	poetry run black $(pyobjs)

bandit:
	poetry run bandit --verbose $$(find src -regex .*\.pyi? -not -name test\*)

pytest:
	@echo "==========" "$@" "=========="
	poetry run pytest
# --pylama

pyroma:
	@echo "==========" "$@" "=========="
	poetry run pyroma .

pylint:
	@echo "==========" "$@" "=========="
#	poetry run pylint $(pyobjs)
	-poetry run pylint src/valuefragments/[cdhmv]*.py

pydocstyle:
	@echo "==========" "$@" "=========="
	poetry run pydocstyle $(pyobjs)

pyright: export NODE_OPTIONS = --experimental-worker
pyright:
	@echo "==========" "$@" "=========="
#	-poetry run pyright --verbose $(pyobjs)
	-poetry run pyright src/valuefragments
#	-poetry run pyright --verifytypes valuefragments

./typings/src/valuefragments/contextmanagers.pyi ./typings/src/valuefragments/decorators.pyi ./typings/src/valuefragments/helpers.pyi ./typings/src/valuefragments/test_helpers.pyi ./typings/src/valuefragments/__init__.pyi: src/valuefragments/contextmanagers.py src/valuefragments/decorators.py src/valuefragments/helpers.py src/valuefragments/test_helpers.py src/valuefragments/__init__.py
	-poetry run pyright --createstub src/valuefragments

pylama:
	@echo "==========" "$@" "=========="
	poetry run pylama src

install:
	sudo python3 -m pip install --upgrade --user --editable .

pyre: $(pyobjs) pyreinfer pyrecheck .watchmanconfig .pyre_configuration
	poetry run pyre init #only once

pyreinfer:
# Try adding type annotations to untyped codebase.
	poetry run pyre infer --print-only --debug-infer

pyreanalyse:
# Run Pysa, the inter-procedural static analysis tool.
	mkdir -p pyreanalysis
	poetry run pyre analyze --save-results-to pyreanalysis
	
pyrecheck:
	poetry run pyre --no-sequential --number-of-workers=3 --noninteractive --show-error-traces

requirements.txt: poetry.lock
	poetry export --without-hashes --with dev --output $@

pytype:
	poetry run pytype --keep-going --jobs 4 $(pyobjs)

ruff:
	poetry run ruff check --fix src/valuefragments/[dch]*.py

cythontest:
	-rm src/valuefragments/mathhelpers.cpython*
	cd src; poetry run python -m timeit -s "from valuefragments.mathhelpers import loanrate" "loanrate(250000,0.03,15)"
	cd src/valuefragments; poetry run cythonize -a -i mathhelpers.py
	cd src; poetry run python -m timeit -s "from valuefragments.mathhelpers import loanrate" "loanrate(250000,0.03,15)"
