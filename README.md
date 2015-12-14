# Fall 2015 - Project Lambda
[![Build Status](https://travis-ci.org/berkeley-stat159/project-lambda.svg?branch=master)](https://travis-ci.org/berkeley-stat159/project-lambda?branch=master)
[![Coverage Status](https://coveralls.io/repos/berkeley-stat159/project-lambda/badge.svg?branch=master)](https://coveralls.io/r/berkeley-stat159/project-lambda?branch=master)

## System requirements
### Storage
The raw data is approximately 37.5 GBs. Additionally, the complete analysis will - in total - produce another approximately 190 GBs of data written to disk. Please ensure your machine is equippted with sufficient storage space. 
### Memory
Since large matrices must be computed and held in memory, systems should have at least 90 GBs of accessible RAM. **We strongly encourage running on a machine with 120 GBs of accessible RAM to emulate development environment.** 


## Installation
1. Clone and move into the project repository: `git clone https://github.com/berkeley-stat159/project-lambda.git && cd project-lambda`
2. Install python dependencies with pip: `pip install -r requirements.txt`
3. Code depends on an internally provided python module module called `stat159lambda`. Ensure this module is on your python path with `export PYTHONPATH='<absolute-path-to-repository>/project-lambda/code'`.  
For example, `export PYTHONPATH='/Users/alondaks/project-lambda/code'`. We strongly encourage adding your export statement to your `.bashrc` while running this project to ensure the environement variable is defined in all shells. 

## Environment Variables
Data for a single subject is ~7.5 GBs due to 2 hour scan at 7 Tesla resolution. The preprocessing scripts are therefore memory intensive. Reproducing preprocessing code should be on a machine with 70+ GBs. In addition to downloading raw data, ``make data`` from the root project directory will download all preprocessed data. Setting a unix environment variable ``USE_CACHED_DATA`` will instruct scripts if they reexecute preprocessing or not. ``USE_CACHED_DATA='True'`` will bypass any presprocessing as long as the resulting preprocessed file exists in ``data/processed/``. ``USE_CACHED_DATA='False'`` will recalculate preprocessed files even if they exist in ``data/processed/``. ``USE_CACHED_DATA`` will default ``'True'``.



## Collaborators
- Alon Daks ([`alondaks`](https://github.com/alondaks))
- Jordeen Chang ([`jodreen`](https://github.com/jodreen))
- Lisa Ann Yu ([`lisaannyu`](https://github.com/lisaannyu))
- Ying Luo ([`yingtluo`](https://github.com/yingtluo))
