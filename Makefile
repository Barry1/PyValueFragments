
.PHONY = default build buildprep install

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

build: buildprep
	python3 -m build

buildprep:
	@sudo apt-get install --assume-yes python3-venv
	@python3 -m pip install --user --upgrade build

install:
	sudo python3 -m pip install --upgrade --user --editable .
