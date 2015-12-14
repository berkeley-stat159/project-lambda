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


data:
	cd data && make data

validate-data:
	cd data && make validate

preprocess:
	python code/stat159lambda/preprocess/preprocess.py

eda:
	python code/stat159lambda/reproduction/inter_run_diagnostics.py
	python code/stat159lambda/simulations/correlation_simulation.py

reproduction:
	python code/stat159lambda/reproduction/similarity.py
	python code/stat159lambda/reproduction/analyze_similarity.py

classification-cross-validate:
	python code/stat159lambda/classification/rf_cross_validate.py

classification-validation:
	python code/stat159lambda/classification/rf_validation.py

all-analysis:
	make preprocess
	make eda
	make reproduction
	make classification
	make classification-cross-validate
	make classification-validation