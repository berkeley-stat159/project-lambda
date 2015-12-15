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


download-data:
	cd data && make download-data

validate-data:
	cd data && make validate

preprocess:
	python code/stat159lambda/preprocess/preprocess.py

eda:
	python code/stat159lambda/reproduction/inter_run_diagnostics.py
	python code/stat159lambda/reproduction/brain_mask.py
	python code/stat159lambda/simulations/correlation_simulation.py

reproduction:
	python code/stat159lambda/reproduction/similarity.py
	python code/stat159lambda/reproduction/analyze_similarity.py

classification-cross-validate:
	python code/stat159lambda/classification/random_forest/rf_cross_validate.py

classification-validation:
	python code/stat159lambda/classification/random_forest/rf_validation.py

generate-paper:
	cd paper && make all

clean-paper:
	cd paper && make clean