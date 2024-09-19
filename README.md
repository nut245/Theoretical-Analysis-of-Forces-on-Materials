# Theoretical-Analysis-of-Forces-on-Materials
A python project undertaken to complete a physics research report

The Theoretical Analysis of Forces on Materials Library simulates given materials 
under tensile stresses, to investigate the capabilities and strengths of materials 
in a controlled and comparable manner. It is made up of modules and files with 
sequential purposes. One of which being 'DataGeneration' that produces an excel 
file of data of a material's tensile stress and strain. And 'Plotting' to 
showcase such data consistantly.

## Table of contents

- Requirements
- Installation
- Configuration
- Maintainers

## Requirements

This Library requires the following modules:

- [DataGeneration](DataGeneration\TensileStressStrainValues.py)
- [Plotting](Plotting\PlottingStressStrainCurve.py)

## Installation

The required modules need external installation of 3rd party Python libraries through pip.
These consist of 'openpyxl' (for DataGeneration module); as well as 'numpy', 'pandas', and 
'matplotlib' (for Plotting module). The last requirement is to run the Python files of 
respective modules. All potential auxiliary files will not run, as they are missing the 
validation to check whether it was the __main__ file.

## Configuration

1. Go to DataGeneration (module) » SubstanceProperties.txt
2. Edit/change desired attribute of material, for example "Ultimate_Tensile_Strength"
3. Save and reload entire directory to see effects of changes

Documentation is available per file for what each tasks are being performed
affects.

## Maintainers

- Imran Almashoor
