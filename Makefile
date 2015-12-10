.PHONY: all clean coverage test

all: clean

clean:
	find . -name "*.so" -o -name "*.pyc" -o -name "*.pyx.md5" | xargs rm -f

coverage:
	nosetests code/stat159lambda/ data --with-coverage

test:
	nosetests code/stat159lambda/ data

verbose:
	nosetests -v code/stat159lambda/ data
