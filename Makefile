.PHONY=default build buildprep install


default:
	autopep8 --in-place *.py
	isort *.py
	black *.py
	pylama *.py
	pylint *.py

build: buildprep
	python3 -m build

buildprep:
	@sudo apt-get install --assume-yes python3-venv
	@python3 -m pip install --user --upgrade build

install:
	sudo python3 -m pip install --upgrade --user --editable .









