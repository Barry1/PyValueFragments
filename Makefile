.PHONY = default build buildprep install pyre pyreanalyse pyrecheck pyreinfer pytype
#should max-load be num-cpus?
MAKEFLAGS += --jobs --max-load=2 --output-sync=target
#https://www.gnu.org/software/make/manual/html_node/Wildcard-Function.html
#PYOBJS = $(wildcard *.py)
#pyobjs:= $(shell tree -if | egrep .pyi?$$)
#pyobjs:= $(shell find src -regex .*pyi?$$)
pyobjs!= find src -regex .*\.pyi?$$

default: formatters pylint pydocstyle pylama pyright checkminver

checkminver:
	poetry run vermin -v --no-parse-comments --backport typing src

formatters:
	@echo "==========" "autopep8" "=========="
	poetry run autopep8 $(pyobjs)
	@echo "==========" "isort" "=========="
	poetry run isort $(pyobjs)
	@echo "==========" "black" "=========="
	poetry run black $(pyobjs)

pylint:
	@echo "==========" "$@" "=========="
	poetry run pylint $(pyobjs)

pydocstyle:
	@echo "==========" "$@" "=========="
	poetry run pydocstyle $(pyobjs)

pyright: export NODE_OPTIONS = --experimental-worker
pyright:
	@echo "==========" "$@" "=========="
	-pyright --dependencies --stats --verbose $(pyobjs)
	-pyright --verifytypes valuefragments

./typings/src/valuefragments/contextmanagers.pyi ./typings/src/valuefragments/decorators.pyi ./typings/src/valuefragments/helpers.pyi ./typings/src/valuefragments/test_helpers.pyi ./typings/src/valuefragments/__init__.pyi: src/valuefragments/contextmanagers.py src/valuefragments/decorators.py src/valuefragments/helpers.py src/valuefragments/test_helpers.py src/valuefragments/__init__.py
	-poetry run pyright --createstub src/valuefragments

pylama:
	@echo "==========" "$@" "=========="
	poetry run pylama .

install:
	sudo python3 -m pip install --upgrade --user --editable .

pyre: $(pyobjs) pyreinfer pyrecheck .watchmanconfig .pyre_configuration
#	pyre init #only once

pyreinfer:
# Try adding type annotations to untyped codebase.
	pyre infer --print-only --debug-infer

pyreanalyse:
# Run Pysa, the inter-procedural static analysis tool.
	mkdir -p pyreanalysis
	poetry run pyre analyze --save-results-to pyreanalysis --use-cache

pyrecheck:
	poetry run pyre check

requirements.txt: poetry.lock
	poetry export --without-hashes --dev --output $@

pytype:
	poetry run pytypy $(pyobjs)
