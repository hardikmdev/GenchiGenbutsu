"""
Created on  11 - July -2018

Author: HD
"""
import sqlite3
import json

from pip._vendor.urllib3.util import retry

import HD_utils
import re

#from scratch import q

""" 


"""


class SqlLiteDb:

    def __init__(self, db_filename='tmp.db'):  # Constructor
        self.__filename = db_filename
        # sqlite3.enable_callback_tracebacks(True)
        # self.__db = sqlite3.connect(db_filename)
        self.__db = sqlite3.connect(db_filename, detect_types=sqlite3.PARSE_DECLTYPES,timeout=10)
        self.__dbc = self.__db.cursor()
        self.__table_name = None
        self.__table_lst = HD_utils.listOfTupleToTupleStr(self.__dbc.execute("SELECT name FROM sqlite_master WHERE type='table';").fetchall())
        print self.__table_lst
        self.__table_attrs = None

    def db_create_table(self, table_name=None, table_attr=None):
        print(' Posting : create table ' + table_name + ' (' + str(table_attr)[1:-1] + " INT DEFAULT 0)")
        try:
            self.__dbc.execute('''create table ''' + table_name + ' ' + str(table_attr) + "INT DEFAULT 0)")
            # self.__table_name = table_name
            # self.__table_attrs = table_attr
        except sqlite3.OperationalError:
            print('SQL statement failed with Operational error' + str(sqlite3.OperationalError.message))
        # self.__table_name = [self.__table_name.append(table_name) if table_name not in self.__table_name]
        if table_name not in self.__table_lst:
            self.__table_lst.append(table_name)
        self.__table_name = table_name
        # self.__table_attrs = table_attr

    def db_drop_table(self,table_name=None):
        self.__dbc.execute('''DROP TABLE IF EXISTS''' + table_name)
        self.__db.commit()

    def db_add_data(self,table_name=None, table_attr=None, val_str=None):
        if len(table_attr) == len(val_str):
            q_str = ''' INSERT INTO ''' + table_name + str(table_attr) + ' VALUES' + str(val_str)
            # print(' Posting : ' + q_str)
        else:
            print(' Caution : len(table_attr) != len(val_str)\n')
            q_str = ''' INSERT INTO ''' + table_name + ' VALUES' + str(val_str)
            # print(' Posting : ' + q_str)

        print(' Posting : ' + q_str)
        # try:
        self.__dbc.execute(q_str)
        self.__db.commit()
        print ("Records created successfully")
        # except sqlite3.OperationalError as e:
            # print('[-] Sqlite operational error: {}, account: {} Retrying...'.format(e))
        # except sqlite3.InterfaceError as e:
            # print('[-] Sqlite interface error: {}, account: {} Retrying...'.format(e))
        # except sqlite3.OperationalError:
            # sqlite3.OperationalError
            #print('SQL statement failed with Operational error' + str(sqlite3.OperationalError.message))

    def db_add_multiple_data(self,table_name=None, table_attr=None, val_lst=None):

        for val in val_lst:
            # val_str = tuple(map(HD_utils.safeStr, val))
            val_str = HD_utils.tupleToStr(val)
            if len(table_attr) == len(val_str):
                q_str = ''' INSERT INTO ''' + table_name + str(table_attr) + ' VALUES' + str(val_str)
                # print(' Posting : ' + q_str)
            else:
                q_str = ''' INSERT INTO ''' + table_name + ' VALUES' + str(val_str)
                print(' Caution : len(table_attr) != len(val_str)\n')
                # print(' Posting : ' + q_str)

            # q_str = ''' INSERT INTO ''' + table_name + str(table_attr) + ' VALUES' + str(val_str)
            print(' Posting : ' + q_str)
            # try:
            self.__dbc.execute(q_str)
            # except sqlite3.OperationalError as e:
                # print('[-] Sqlite operational error: {}, account: {} Retrying...'.format(e))
            # except sqlite3.InterfaceError as e:
                # print('[-] Sqlite interface error: {}, account: {} Retrying...'.format(e))
            # except sqlite3.OperationalError:
                # sqlite3.OperationalError
                # print('SQL statement failed with Operational error' + str(sqlite3.OperationalError.message))

        self.__db.commit()
        print ("Records created successfully")

    def db_unique_add_multiple_data(self,table_name=None, table_attr=None, val_lst=None):

        for val in val_lst:
            # val_str = tuple(map(HD_utils.safeStr, val))
            val_str = HD_utils.tupleToStr(val)
            if len(table_attr) == len(val_str):
                q_str = ''' INSERT INTO ''' + table_name + " " + str(table_attr) + ' SELECT '+ str(val_str)[1:-1] + ' WHERE NOT EXISTS (SELECT 1 FROM ' + table_name + ' WHERE key = "' + str(val_str[0]) + '")'
                # print(' Posting : ' + q_str)
            else:
                q_str = ''' INSERT INTO ''' + table_name + ' SELECT ' + str(val_str)[1:-1] + ' WHERE NOT EXISTS (SELECT 1 FROM ' + table_name + ' WHERE key = "' + str(val_str[0]) + '")'
                print(' Caution : len(table_attr) != len(val_str)\n')
                # print(' Posting : ' + q_str)

            # q_str = ''' INSERT INTO ''' + table_name + str(table_attr) + ' VALUES' + str(val_str)
            print(' Posting : ' + q_str)
            # try:
            self.__dbc.execute(q_str)
            # except sqlite3.OperationalError as e:
                # print('[-] Sqlite operational error: {}, account: {} Retrying...'.format(e))
            # except sqlite3.InterfaceError as e:
                # print('[-] Sqlite interface error: {}, account: {} Retrying...'.format(e))
            # except sqlite3.OperationalError:
                # sqlite3.OperationalError
                # print('SQL statement failed with Operational error' + str(sqlite3.OperationalError.message))

        self.__db.commit()
        print ("Records created successfully")

    def db_transaction(self,trans_str):
        try:
            self.__dbc.execute(trans_str)
            self.__db.commit()
        except sqlite3.OperationalError:
            print('SQL statement failed with Operational error')

    def update_query_build (self,q_key,t_name,up_or_down):
        # data.execute("UPDATE sample SET rank = rank + 1 WHERE key=?", [inpt])
        q_str = ''''''
        count = len(self.__table_lst)
        fetch_conf = '''SELECT confidence_rank FROM ''' + t_name + ''' WHERE key=''' + "'" + q_key + "' COLLATE NOCASE"
        conf_rank = self.db_exec_query(fetch_conf)
        print conf_rank
        print fetch_conf
        q_str = q_str + '''UPDATE '''+ t_name + ''' SET confidence_rank = confidence_rank ''' + up_or_down + ''' 1 WHERE key=''' + "'" + q_key + "' COLLATE NOCASE"
        # q_str = q_str + ''' COLLATE NOCASE'''
        print "Posting Query : " + q_str
        ans = self.db_exec_query(q_str)
        return q_str

    def query_build (self,q_key):
        q_str = ''''''
        count = len(self.__table_lst)
        for t_name in self.__table_lst:
            q_str = q_str + '''SELECT key,value,confidence_rank, '''+ "'"+str(HD_utils.safeStr(t_name))+"'" +''' as Source FROM '''
            count = count - 1
            q_str = q_str + str(HD_utils.safeStr(t_name)) + ''' WHERE key = ''' + "'" + str(q_key) + "'"
            q_str = q_str + ''' COLLATE NOCASE'''
            if (count > 0):
                q_str = q_str + " union all "

        q_str = q_str + ''' ORDER BY confidence_rank desc'''
        print "Posting Query : " + q_str
        # ans = self.db_post_query(q_str)
        return q_str

    def db_post_query(self, query_str):
        return self.__dbc.execute(query_str).fetchall()
        # self.__db.commit()

    def db_exec_query(self, query_str):
        return self.__dbc.execute(query_str)
        self.__db.commit()

    def db_post_multiple_query(self, query_strs):
        self.__dbc.execute(query_strs)
        self.__db.commit()

    def __del__(self):  # Destructor
        "Close DB Connection"
        self.__db.commit()
        self.__db.close()

    def adapt_json(data):
        return (json.dumps(data, sort_keys=True)).encode()

    def convert_json(blob):
        return json.loads(blob.decode())

    def adapt_json_data(self):
        sqlite3.register_adapter(dict, adapt_json)
        sqlite3.register_adapter(list, adapt_json)
        sqlite3.register_adapter(tuple, adapt_json)
        sqlite3.register_converter('JSON', convert_json)