% Project Lambda Progress Report
% Jordeen Chang, Alon Daks, Ying Luo, Lisa Ann Yu
% November 12, 2015

# Background

## The Paper

- from OpenFMRI.org
- A high-resolution 7-Tesla fMRI dataset from complex natural stimulation with an audio movie
- Purpose: study common and idiosyncratic brain response patterns to complex auditory stimulation

## ABOUT THE DATA

- Brief overview:
    - 20 participants recorded at a high field strength of 7 Tesla while listening to “Forrest Gump”
   - Collected fMRI data for entire movie in .niigz format with additional information regarding movie scenes

- Tools used:
    - MRI scanner and pulse oximetry to conduct blood oxygen level dependent (BOLD) imaging, structural MRI imaging, and physiological assay
- Ultimate goal:
    - Provide data for others to explore auditory cognition, language and music perception, social perception, etc.

## HOW WE CHOSE THE DATA

- Very large data files: for each subject (total of 20), the download size is approximately 16 GB, and that does not even include unzipping all the files inside
- The download for each subject includes a lot of other information besides just the fMRI data
    - Cardiac and respiratory trace, angiographies, structural MRI data
- Three versions of the fMRI data is included:
    - the raw data, the linear alignment, and the non-linear alignment
    - Only be choosing one of them: the one linearly aligned

## ROADBLOCKS & OUR SOLUTIONS
- Dealing with the size of the data: 16 GB per subject, 20 subjects total
    - SOLUTION: Using external hard drive to transfer data between group  members. Working with just Subject 1 for now and applying functions to other subjects.  If time allows, we will try to run code on multiple subjects (e.g. females vs. males)
- Lack of knowing which direction to take thie project
    - SOLUTION:
        - Entire website dedicated to studying this dataset at studyforrest.org
        - Deal with multiple comparisons by using a Bonferroni correction (even though it’s technically too conservative)
        - Attempt to validate our model by running it on other subjects to see if the same voxels are significant
            - Indicates that people respond differently to day vs. night and exterior vs. interior

## CURRENT PROGRESS
- 
## The Method

- Representational similarity analysis
- Dissimilarity matrices -> representational consistency map

# Initial work

## Exploratory Data Analysis

- downloaded data
- simple plots, summary statistics across participants

# Next steps

## Preprocessing / Validation

- 

## Statistical Analysis

- 
