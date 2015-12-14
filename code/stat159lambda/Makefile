test:
	nosetests utils

coverage:
	nosetests utils --with-coverage --cover-package=utils 

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

classification:
	python code/stat159lambda/classification/rf_cross_validate.py

all-analysis:
	make preprocess
	make eda
	make reproduction
	make classification