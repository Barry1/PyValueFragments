.PHONY = default build buildprep install pyre pyreanalyse pyrecheck pyreinfer

MAKEFLAGS += --jobs --max-load=3 --output-sync

pyobjs:= *.py valuefragments/*.py

default:
	@echo -n "=========="
	@echo -n "autopep8"
	@echo "=========="
	autopep8 $(pyobjs)
	@echo -n "=========="
	@echo -n "isort"
	@echo "=========="
	isort $(pyobjs)
	@echo -n "=========="
	@echo -n "black"
	@echo "=========="
	black $(pyobjs)
	@echo -n "=========="
	@echo -n "pylama"
	@echo "=========="
	pylama
	@echo -n "=========="
	@echo -n "pylint"
	@echo "=========="
	pylint $(pyobjs)
	@echo -n "=========="
	@echo -n "pydocstyle"
	@echo "=========="
	pydocstyle $(pyobjs)
	@echo -n "=========="
	@echo -n "pylama"
	@echo "=========="
	pylama .

build: buildprep
	python3 -m build

buildprep:
	@sudo apt-get install --assume-yes python3-venv
	@python3 -m pip install --user --upgrade build

install:
	sudo python3 -m pip install --upgrade --user --editable .

pyre: $(pyobjs) pyreinfer pyreanalyse pyrecheck .watchmanconfig .pyre_configuration
#	pyre init #only once

pyreinfer:
# Try adding type annotations to untyped codebase.
	pyre infer --print-only --debug-infer

pyreanalyse:
# Run Pysa, the inter-procedural static analysis tool.
	pyre analyze --save-results-to=./pyreanalysis --use-cache

pyrecheck:
	pyre check