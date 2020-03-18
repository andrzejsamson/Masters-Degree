import xlrd

def openFile(path):
    book = xlrd.open_workbook(path, on_demand=True)
    sheet = book.sheet_by_index(0)
    return sheet.ncols, sheet.nrows

def readValues(path, row, ncols):
    book = xlrd.open_workbook(path, on_demand=True)
    sheet = book.sheet_by_index(0)
    rowValues = list()
    for i in range(ncols):
        try:
            rowValues.append(int(sheet.row(row)[i].value))
        except:
            rowValues.append(sheet.row(row)[i].value)
    return rowValues

def readColumns(path, col, nrows):
    book = xlrd.open_workbook(path, on_demand=True)
    sheet = book.sheet_by_index(0)
    colValues = list()
    for i in range(nrows):
        try:
            colValues.append(int(sheet.row(i)[col].value))
        except:
            colValues.append(sheet.row(i)[col].value)
    return colValues
