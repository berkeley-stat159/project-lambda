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

## How to run code and analysis
Please run the follow make commands in order from top to bottom.  

1. Download and verify data    
  - `make data` fetches and downloads raw data  
  - `make validate-data` verifies data integrity against known checksums  
2. Preprocess the data 
  - `make preprocess` concatenates runs, applies guassian filter, and reshapes data to 2d 
3. Exploratory data analysis 
  - `make eda` produces eda plots and simulations 
4. Reproduction 
  - `make reproduction` runs all correlation reproduction work and produces analysis figures 
5. Classification 
  - `make classification-cross-validate` runs random forrest cross validation and saves cv accuracies to file 
  - `make classification-validation` tests a fully trained random forrest on validation set and saves accuracy to file 



## Collaborators
- Alon Daks ([`alondaks`](https://github.com/alondaks))
- Jordeen Chang ([`jodreen`](https://github.com/jodreen))
- Lisa Ann Yu ([`lisaannyu`](https://github.com/lisaannyu))
- Ying Luo ([`yingtluo`](https://github.com/yingtluo))

*Special thank you to Jarrod Millman, Matthew Brett, Ross Barnowski, and J-B Poline for their continued support, instruction and encouragment with this project*
