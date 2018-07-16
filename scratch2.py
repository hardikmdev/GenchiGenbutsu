import os
import win32com.client
import xlrd
import itertools

from pandas import *

import HD_xl_parser
import HD_db
import HD_utils

baseDir = 'D:\Myfolder\Study\py\ChatterBot'
s_name = 'AT.xlsx'
db_name = 'sample.db'
table_name = 'Excel_Data'

file_path = os.path.join(baseDir, s_name)
db_path = os.path.join(baseDir, db_name)
file_name, file_extension = os.path.splitext(file_path)

dataList = []

# method 1
xlApp = win32com.client.Dispatch("Excel.Application")   # Calls for Excel
xlWb = xlApp.Workbooks.Open(file_path)  # It finds the workbook
xlSht = xlWb.Worksheets(1)

# method 2
wb = xlrd.open_workbook(file_path)

# method 3
xls = ExcelFile(file_path)
df = xls.parse(xls.sheet_names[0])
dd = df.to_dict()

# Method 4
obj = HD_xl_parser.Excel(file_path)
r = obj.get_range_by_cells((1,1),(obj.nrows,obj.ncols))
dt = dict(zip((v[0] for v in r.Value), (v[1] for v in r.Value)))
# adt = dict(itertools.izip((v[0] for v in r.Value), (v[1] for v in r.Value)))
# string_tuple_list = [tuple(map(str,eachTuple)) for eachTuple in data_range]

data_range = obj.get_contiguous_range()
db_obj = HD_db.SqlLiteDb(db_path)

# string_attr_list = tuple(map(HD_utils.safeStr,data_range[0]))
string_attr_create_list = ('key','value','ref','info','add','confidence_rank')
var_string_attr_list = ('key','value','ref','info','add')


db_obj.db_create_table(table_name,string_attr_create_list)

# db_obj.db_add_data(db_obj._SqlLiteDb__table_name,var_string_attr_list,tuple(map(HD_utils.safeStr,data_range[1])))

# for db_data in  data_range[1:]:
    # db_obj.db_add_data(db_obj._SqlLiteDb__table_name,db_obj._SqlLiteDb__table_attrs,tuple(map(HD_utils.safeStr,db_data)))

# db_obj.db_add_multiple_data(db_obj._SqlLiteDb__table_name,var_string_attr_list,data_range[1:])
db_obj.db_unique_add_multiple_data(db_obj._SqlLiteDb__table_name,var_string_attr_list,data_range[1:])

# db_obj.__del__()