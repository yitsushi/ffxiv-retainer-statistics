.PHONY: all clean

all:
	python setup.py develop

dist: clean
	python setup.py bdist bdist_wheel

clean:
	rm -rf dist build
