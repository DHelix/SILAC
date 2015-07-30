import xlrd
import csv

def xls2csv(xlsFile,csvFile):
	wb = xlrd.open_workbook(xlsFile)
	sh = wb.sheet_by_index(0)
	csvFile = open(csvFile, 'wb')
	wr = csv.writer(csvFile, quoting=csv.QUOTE_ALL)
	for row in range(sh.nrows):
		singleRow=[]
		for col in range(sh.ncols):
			val=sh.cell_value(row, col)
			if isinstance(val, unicode):
				val=val.encode('utf8')
			singleRow.append(val)
		wr.writerow(singleRow)
	csvFile.close()