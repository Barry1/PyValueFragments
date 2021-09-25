.PHONY = default build buildprep install pyre pyreanalyse pyrecheck pyreinfer

MAKEFLAGS += --jobs --max-load=3 --output-sync=target

pyobjs:= $(shell tree -if | egrep .pyi?$$)

default: formatters pylint pydocstyle pylama pyright checkminver

checkminver:
	poetry run vermin -v --backport typing src

formatters:
	@echo "==========" "autopep8" "=========="
	autopep8 $(pyobjs)
	@echo "==========" "isort" "=========="
	isort $(pyobjs)
	@echo "==========" "black" "=========="
	black $(pyobjs)

pylint:
	@echo "==========" "$@" "=========="
	pylint $(pyobjs)

pydocstyle:
	@echo "==========" "$@" "=========="
	pydocstyle $(pyobjs)

pyright: export NODE_OPTIONS = --experimental-worker
pyright:
	@echo "==========" "$@" "=========="
	-pyright --dependencies --stats --verbose $(pyobjs)
	-pyright --verifytypes valuefragments
	-pyright --createstub valuefragments

pylama:
	@echo "==========" "$@" "=========="
	pylama .

build: buildprep
	python3 -m build

buildprep:
	@sudo apt-get install --assume-yes python3-venv
	@python3 -m pip install --user --upgrade build

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
	pyre analyze --save-results-to pyreanalysis --use-cache

pyrecheck:
	pyre check

requirements.txt: poetry.lock
	poetry export --without-hashes --dev --output $@
