
.PHONY = default build buildprep install

pyobjs:= *.py valuefragments/*.py
default:
	@echo ===================================================================
	-autopep8 --in-place --jobs 0 --recursive $(pyobjs)
	@echo ===================================================================
	-isort * $(pyobjs)
	@echo ===================================================================
	-black --target-version py37 $(pyobjs)
	@echo ===================================================================
	-pylama
	@echo ===================================================================
	-pylint $(pyobjs)

build: buildprep
	python3 - m build

buildprep:
	@sudo apt-get install --assume-yes python3-venv
	@python3 - m pip install --user --upgrade build

install:
	sudo python3 - m pip install --upgrade --user --editable .
