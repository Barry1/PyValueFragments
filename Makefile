.PHONY: vermin
#https://www.gnu.org/software/make/manual/html_node/Wildcard-Function.html
#PYOBJS = $(wildcard *.py)
#PYOBJS != find . -regex \.pyi?$
PYOBJS != find src -regex .*\.pyi?$$

vermin:
	poetry run vermin -v --backport typing $(PYOBJS)
