# SILAC
A Python script to search and filter SILAC result based on customizable criteria and automatically retrieve gene information from online database.

## Author: 
DHelix

## Version: 
3.0

## Date: 
July 19, 2013

## Function:
- Read a .csv file; or read a .xls file and convert it to a .csv file.
- Search based on a given patter and a given H/L range.
- Automatically find gene's full name based on IPI number, and also include the web page link to that gene.
- Write the searching result into a new csv file.

## Usage: 
python SILAC_IPI.py [inputFileName] [OutputFileName]  

##Note:
Please include xls2csv.py (convert .xls files to .csv files) and ipi.HUMAN.xrefs.txt (see Update) in the same directory.

## Update:
Since IPI service was shut down. Use downloaded the last release for searching.
