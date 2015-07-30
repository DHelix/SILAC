# Author: Dan Jin
# Version: 3.0
# Date: July 19, 2013
# Function:
#	-Read a .csv file; or read a .xls file and convert it to a .csv file.
#	-Search based on a given patter and a given H/L range.
#	-Automatically find gene's full name based on IPI number, and also include the web page link to that gene.
#	-Write the searching result into a new csv file.
# Usage: python SILAC3.py [inputFileName] [OutputFileName]
# Update:
# Since IPI service was shut down. Use downloaded the last release for searching.

# import library
import sys
import csv
import re
import urllib
import xls2csv



# Import ipi.HUMAN.xrefs
print "Importing ipi.HUMAN.xrefs..."
# read csv file
IPIxrefs = list(csv.reader(open("ipi.HUMAN.xrefs.txt",'rU'),delimiter='\t'))
print "Done importing ipi.HUMAN.xrefs"
# print basic info about the list: the number of records and the length of each record
print "\nthe length of list: %d\n" %((len(IPIxrefs))-2)
print "the number of element in each record: %d\n" %(len(IPIxrefs[1]))
# Get the number of column
for i in range(len(IPIxrefs[2])):
	if IPIxrefs[1][i]=='IPI':
		IPI=i
	if IPIxrefs[1][i]=='HGNC,SYM':
		HGNC=i
	if IPIxrefs[1][i]=='NCBI,SYM':
		NCBI=i
	if IPIxrefs[1][i]=='REFSEQ GI':
		GI=i


# Ask for input and output file names.
if len(sys.argv[1:]) == 2:
	[inFileNameRaw,outFileName]=sys.argv[1:3]
elif len(sys.argv[1:]) == 1:
	inFileNameRaw = sys.argv[1]
	outFileName = 'result.csv'
else:
	print "Need input and output file names."
	inFileNameRaw = str(raw_input("Please enter file names for reading from:"))
	outFileName = str(raw_input("Please enter file names for writing into:"))
print "Opening", inFileNameRaw


# Check input file's format. if it is not a csv file, convert it to csv file using xls2csv function
fileFormat=re.compile('[Cc][Ss][Vv]$')
if (re.search(fileFormat,inFileNameRaw)==None):
	inFileName=inFileNameRaw[:-4]+'.csv' # generate new input file name with .csv
	xls2csv.xls2csv(inFileNameRaw,inFileName) # Convert file to csv
	print "Done converting %s to %s!\n" %(inFileNameRaw,inFileName)
else:
	inFileName=inFileNameRaw


# Ask for comparison method and H/L range
compMethod = str(raw_input("Please choose a method: == / >= / > / <= / < / () / []: "))
while (compMethod == ''):
	print "Please choose a comparison method: == / >= / > / <= / < / () / []: "
	compMethod = str(raw_input("Please choose a method:"))

if (compMethod == '==') or (compMethod == '>=') or (compMethod == '>') or (compMethod == '<=') or (compMethod == '<'):
	HLRatio=float(raw_input("Please enter a threshold:"))
	print "Find H/L ratio %s %0.2f" %(compMethod, HLRatio)
elif compMethod == '()':
	HLRange=[0.0,0.0]
	(HLRange[0],HLRange[1])=float(raw_input("Lower bound:")),float((raw_input("Upper bound:")))
	if HLRange[0] > HLRange[1]:
		print "Error! The first number should be smaller than the second one!\nPlease re-enter:"
		(HLRange[0],HLRange[1])=float(raw_input("Lower bound:")),float((raw_input("Upper bound:")))
	print "Find H/L ratio between: (%0.2f,%0.2f)" %(HLRange[0],HLRange[1])
elif compMethod == '[]':
	HLRange=[0.0,0.0]
	(HLRange[0],HLRange[1])=float(raw_input("Lower bound:")),float((raw_input("Upper bound:")))
	if HLRange[0] > HLRange[1]:
		print "Error! The first number should be smaller than the second one!\nPlease re-enter:"
		(HLRange[0],HLRange[1])=float(raw_input("Lower bound:")),float((raw_input("Upper bound:")))
	print "Find H/L ratio between: [%0.2f,%0.2f]" %(HLRange[0],HLRange[1])


# count the number of record that match the searching pattern
numberOfRecord=0
# define searching pattern
inputPattern=str(raw_input("\nPlease enter searching pattern (use '?' for any single char; use '[]' for alternative chars at the same position; use '.*' to find ALL sequence): "))
pattern=re.sub('\?','\w',inputPattern)

# read csv file
inFile=list(csv.reader(open(inFileName,'rU'),delimiter=','))
# print basic info about the list: the number of records and the length of each record
print "\nthe length of list: %d\n" %(len(inFile)),
print "the number of element in each record: %d\n" %(len(inFile[1]))
# Get the number of column
for i in range(len(inFile[0])):
	if inFile[0][i]=='Protein Accessions':
		IPI=i
	if inFile[0][i]=='Heavy/Light':
		HL=i
	if inFile[0][i]=='Sequence':
		SQ=i

# write records to new csv
outFile=csv.writer(open(outFileName,'wb'))
# print the head of the table
tableHead=inFile[0]
tableHead.append('NCBI ID')
tableHead.append('Gene Symbol')
tableHead.append('Gene Full Name')
tableHead.append('For more info about this gene, please click here:')
outFile.writerow(tableHead)


# Select the record match certain rules
for i in range(1,len(inFile)):
	if (inFile[i][HL] !=''):
		# Check if given pattern is in each record
		patternMatch=re.findall(pattern,inFile[i][SQ])
		
		# Check if HL ratio is in the giving range
		if compMethod == '==':
			compResult= (float(inFile[i][HL]) == HLRatio)
		elif compMethod == '>=':
			compResult= (float(inFile[i][HL]) >= HLRatio)
		elif compMethod == '>':
			compResult= (float(inFile[i][HL]) > HLRatio)
		elif compMethod == '<=':
			compResult= (float(inFile[i][HL]) <= HLRatio)
		elif compMethod == '<':
			compResult= (float(inFile[i][HL]) < HLRatio)
		elif compMethod == '()':
			compResult= ((float(inFile[i][HL]) > HLRange[0]) & (float(inFile[i][HL]) < HLRange[1]))
		elif compMethod == '[]':
			compResult= ((float(inFile[i][HL]) >= HLRange[0]) & (float(inFile[i][HL]) <= HLRange[1]))
		
		# Check if both rules are met 
		if (patternMatch!=[]) & (compResult):
			numberOfRecord =numberOfRecord+1
			
			# print searching result
			print "Find %s in Record %d, %s: %s with H/L: %0.2f" %(patternMatch, i,inFile[i][IPI], inFile[i][SQ], float(inFile[i][HL]))
			
			# Get the IPI number WITHOUT version number
			IPI0=(re.search('(?<=IPI:)\w+', inFile[i][IPI])).group(0)
			# Search in IPIxresfs table to find the corresponding record
			y=0
			for line in IPIxrefs:
				if IPI0 in line:
					y=1
					HGNCIDSym=line[HGNC]
					NCBIIDSym=line[NCBI]					
			
					# Get the gene info from IPIxrefs table
					NCBIID = re.search('(?<!,)\w+', NCBIIDSym)
					print 'NCBI ID: ', NCBIID.group(0)
					inFile[i].append(NCBIID.group(0))

					NCBISym = re.search('(?<=,)\w+', NCBIIDSym)
					if NCBISym <> '':
						print 'NCBI symble: ', NCBISym.group(0)
						inFile[i].append(NCBISym.group(0))
					else:
						print 'No gene name found.'
						inFile[i].append('No gene name found.')
					
					# Get HGNC ID
					HGNCID = re.search('(?<!,)\w+', HGNCIDSym)
					#print 'HGNC ID: ', HGNCID.group(0)
					#inFile[i].append(HGNCID.group(0))
					
					# Get gene's full name from HGNC
					HGNCurl='http://www.genenames.org/data/hgnc_data.php?hgnc_id='+HGNCID.group(0)
					fbhandle = urllib.urlopen(HGNCurl)
					for line in fbhandle.readlines():
						line=line.rstrip().split('</div>')
						for item in line:
							if "symbol_data-data-app_name" in item:
								geneFullName=item.strip('\t')
								geneFullNameTrim=((re.compile('<td class="symbol_data-data-app_name"><strong>(.*?)</strong></td>')).search(geneFullName)).group(1)
								print 'Gene Full Name: ', geneFullNameTrim
								inFile[i].append(geneFullNameTrim)
				
					# print the NCBI url of the gene
					url='http://www.ncbi.nlm.nih.gov/gene/'+NCBIID.group(0)
					inFile[i].append(url)
					print "For more info about this gene, please click here: ", url, '\n'
			if y==0:
				print 'No record found in ipi.HUMAN.xrefs.txt\n'
			
			# write searching result into a new csv file
			outFile.writerow(inFile[i])

print numberOfRecord, " record(s) found matching the searching pattern."
				
# End of this program
print "\nDone reading", inFileName,
print "\nDone writing", outFileName

