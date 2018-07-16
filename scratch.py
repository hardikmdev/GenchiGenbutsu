import os.path
import win32com.client
from collections import defaultdict
import sqlite3, re
import HD_db, HD_utils

# Calling the Disptach method of the module which
# interact with Microsoft Speech SDK to speak
# the given input from the keyboard
speaker = win32com.client.Dispatch("SAPI.SpVoice")

baseDir = 'D:\Myfolder\Study\py\ChatterBot'
# f_name = 'SRS_SMART.docx'
f_name = 'testdoc.docx'

db_name = 'sample.db'

table_name = 'Word_Data'
db_path = os.path.join(baseDir, db_name)
db_obj = HD_db.SqlLiteDb(db_path)

os.environ['PATH'] = os.environ['PATH'] + ';' + baseDir

word = win32com.client.Dispatch("Word.application")

file_path = os.path.join(baseDir, f_name)
file_name, file_extension = os.path.splitext(file_path)

# string_attr_list = '''(SNo INT, key TEXT, value TEXT, confidence INT)'''
# db_obj.db_create_table(table_name, string_attr_list)


wordObj = word.Documents.Open(file_path, False, False, False)

# check if doc or docx
if file_extension.lower() == '.doc': #
    docx_file = '{0}{1}'.format(file_path, 'x')
    if not os.path.isfile(docx_file):  # Skip conversion where docx file already exists
        print('Converting: {0}'.format(file_path))
        try:
            wordObj = word.Documents.Open(file_path, False, False, False)
            wordObj.SaveAs2(docx_file, FileFormat=16)
            wordObj.Close()
        except Exception:
            print('Failed to Convert: {0}'.format(file_path))


# print("Enter the word you want to speak it out by computer")
# s = input()
# speaker.Speak(s)

# let's get text data
q=wordObj.Content.text
p=wordObj.Content.text

p.split('\r')

spl = p.split()
d = defaultdict(list)
dic = {}

x=zip(p.split(),p.split()[1:])

for k,y in x:
    dic[k]=y


#for a,b in zip(spl, spl[1:]):
#    d[a.translate(None,".,")].append(b.translate(None,".,"))
#print(d)
def_list = []
counter = 0

for para in wordObj.Paragraphs:
    #counter += 1
    Text = para.Range.Text.encode('utf8')
    # print "paragraph to edit:", counter, ":"
    # print str(Text)
    # print str(Text).encode('ascii', 'replace')
    record = re.split(':|\r', Text)
    record.remove("")
    record.append("0")
    record = tuple(record)
#    print record
    def_list.append(record)

# string_attr_list = ('key','value','ref DEFAULT NULL','info DEFAULT NULL','add. DEFAULT NULL','confidence_rank DEFAULT 0')
header_create_tuple = ("key", "value", "confidence_rank")
var_header_tuple = ("key", "value", "confidence_rank")

db_obj = HD_db.SqlLiteDb(db_path)
db_obj.db_create_table(table_name,header_create_tuple)
# db_obj.db_add_multiple_data(table_name,var_header_tuple,def_list)
db_obj.db_unique_add_multiple_data(db_obj._SqlLiteDb__table_name,var_header_tuple,def_list)

# db_obj.__del__()