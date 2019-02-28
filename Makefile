.PHONY: all clean

all: clean
	python setup.py bdist bdist_wheel

clean:
	rm -rf dist build
