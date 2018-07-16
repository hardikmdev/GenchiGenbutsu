import sqlite3
conn = sqlite3.connect('example.db')
data = conn.cursor()


# create data

data.execute("DROP TABLE IF EXISTS sample")
data.execute('''CREATE TABLE sample
             (s_no int, key text, value text, rank int)''')

# insert demo data
data.execute("INSERT INTO sample VALUES ('1','CBTC','Communication Based Controle System',1)")
data.execute("INSERT INTO sample VALUES ('1','ATC','Automatic Train Control',1)")
data.execute("INSERT INTO sample VALUES ('1','ATO','Automatic Train Operation ',1)")
data.execute("INSERT INTO sample VALUES ('1','ATP','Automatic Train Protection',1)")
data.execute("INSERT INTO sample VALUES ('1','CSR','Central system router',1)")

# Save (commit) the changes
conn.commit()

for row in data.execute('SELECT * FROM sample'):
        print row

# data.execute("SELECT * FROM sample WHERE key='{}'".format(text))
# data.execute("SELECT value FROM sample")

# for row in data.execute("SELECT value FROM sample WHERE key = 'CBTC'"):
#        print row
inpt = raw_input("Enter key: ")

# def select_task_by_priority(data):

#    cur = conn.cursor()
data.execute("SELECT value FROM sample WHERE key=?", [inpt])
rows = data.fetchall()
#
for row in rows:
    print(row)
answer = raw_input("Appropriate Answer?: ")
if answer=="Yes":
    data.execute("UPDATE sample SET rank = rank + 1 WHERE key=?", [inpt])
if answer=="No":
    data.execute("UPDATE sample SET rank = rank - 1 WHERE key=?", [inpt])
conn.commit()

f_qry = ''' 
select * from Excel_Data2 where Acronym = 'SRS' union all select * from Excel_Data where Acronym = 'SRS' 
'''