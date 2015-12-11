# Fall 2015 - Project Lambda
[![Build Status](https://travis-ci.org/berkeley-stat159/project-lambda.svg?branch=master)](https://travis-ci.org/berkeley-stat159/project-lambda?branch=master)
[![Coverage Status](https://coveralls.io/repos/berkeley-stat159/project-lambda/badge.svg?branch=master)](https://coveralls.io/r/berkeley-stat159/project-lambda?branch=master)

Team Members: Alon Daks, Lisa Ann Yu, Jordeen Chang, Ying Luo

## Installation 
All code is packaged in a python module called `stat159lambda`.  
Ensure this module is on your python path with `export PYTHONPATH='<path-to-repository>/code'`.  
For example, `export PYTHONPATH='/Users/alondaks/project-lambda/code'`.

## Environment Variables
Data for a single subject is ~7.5 GBs due to 2 hour scan at 7 Tesla resolution. The preprocessing scripts are therefore memory intensive. Reproducing preprocessing code should be on a machine with 70+ GBs. In addition to downloading raw data, ``make data`` from the root project directory will download all preprocessed data. Setting a unix environment variable ``USE_CACHED_DATA`` will instruct scripts if they reexecute preprocessing or not. ``USE_CACHED_DATA='True'`` will bypass any presprocessing as long as the resulting preprocessed file exists in ``data/processed/``. ``USE_CACHED_DATA='False'`` will recalculate preprocessed files even if they exist in ``data/processed/``. ``USE_CACHED_DATA`` will default ``'True'``.

