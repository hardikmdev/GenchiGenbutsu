"""
Created on  11 - July -2018

Author: HD
"""
import win32com.client
import time

""" 
#For older 95-97 Excel Files Use following for faster fetch
from xlrd import open_workbook #xlrd package
wb=open_workbook(r'C:\Users\Prashant\Documents\test1.xls')

s=wb.sheet_by_index(0)
for _ in range(s.nrows):
    for __ in range(s.ncols):
        print s.cell(_,__).value

"""


class Excel:

    def __init__(self, filename=None):  # Constructor
        self.__filename = filename
        self.__xlApp = win32com.client.Dispatch('Excel.Application')

        #if filename:
        try:
            self.__xlwb = self.__xlApp.Workbooks.Open(self.__filename)
            self.sheet = 1
            used = self.__xlwb.Worksheets(1).UsedRange  # First Sheet by Default
            self.nrows = used.Row + used.Rows.Count - 1
            self.ncols = used.Column + used.Columns.Count - 1
        except:
            print "Error Opening " + filename
        #else:
            #self.__xlwb = self.__xlApp.Workbooks.Add()

    def get_cell(self, row, col, sheet=1):
        "Get value of one cell"
        return str(self.__xlwb.Worksheets(sheet).Cells(row, col).Value)

    def set_sheet(self, sheet):
        """
        Set the active worksheet.
        """
        self.sheet = sheet

    def set_cell(self, row, col, value, sheet=1):
        "Set value of one cell"
        self.__xlwb.Worksheets(sheet).Cells(row, col).Value = value
        self.__xlwb.Worksheets(sheet).Columns.AutoFit()

    def save(self, newfilename=None):
        "Saves Excel Sheets"
        if newfilename:
            self.__filename = newfilename
            self.__xlwb.SaveAs(newfilename)
        else:
            self.__xlwb.Save()

    def set_props(self, row, col, **props):
        "Set Cells Properties"
        if props.has_key('sheet'):
            wsc = self.__xlwb.Worksheets(props['sheet']).Cells(row, col)
        else:
            wsc = self.__xlwb.Worksheets(1).Cells(row, col)
        for _ in props:
            if _ == 'FG' or _ == 'fg':
                wsc.GetCharacters(1, len(str(wsc.Value))).Font.ColorIndex = props[_]
            if _ == 'bg' or _ == 'BG':
                wsc.Interior.ColorIndex = props[_]
            elif _ == 'Font' or _ == 'font':
                wsc.Font.Name = props[_]
            elif _ == 'Size' or _ == 'size':
                wsc.Font.Size = 12 + props[_]

    def setcol_width(self, colno, width=0, sheet=1):
        "Set Column Width"
        self.__xlwb.Worksheets(sheet).Columns(colno).ColumnWidth = width

    def get_range_by_cells(self, (cell_start_row, cell_start_col), (cell_end_row, cell_end_col), sheet=1):
        "Get Range of Cells"
        return self.__xlwb.Worksheets(sheet).Range(self.__xlwb.Worksheets(sheet).Cells(cell_start_row, cell_start_col),
                                                   self.__xlwb.Worksheets(sheet).Cells(cell_end_row, cell_end_col))

    def get_contiguous_range(self, row=1, col=1, sheet=1):
        """Tracks down and across from top left cell until it
        encounters blank cells; returns the non-blank range.
        Looks at first row and column; blanks at bottom or right
        are OK and return None within the array"""
        sht = self.__xlwb.Worksheets(sheet)
        # assert isinstance(sht.Range(sht.Cells(row, col), sht.Cells(self.nrows, self.ncols)).Value, object)
        return sht.Range(sht.Cells(row, col), sht.Cells(self.nrows, self.ncols)).Value

    def get_value_by_range(self, s_range):
        """  Get the value of 's_range'."""
        startTime = time.time()
        vals = [v[0] for v in s_range.Value]
        t_time = time.time() - startTime
        return vals

    def mergeRange(self, range):
        "Merge Range of Cells"
        range.Merge()

    def __del__(self):  # Destructor
        "Close XLS Sheet"
        self.__xlApp.Workbooks.Close()
        self.__xlApp.Quit()

