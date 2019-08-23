import os
import sys
import json
import pymysql

from contextlib import closing





def readJson(path, ifNotExists=lambda : print('panic')):
    res = {}
    if not os.path.exists(path):
        ifNotExists()
    with open(path, 'r', encoding='utf8') as fp:
        res = json.load(fp=fp)
    return res

class DB:
    def __init__(self, type, params={}, ifFail=None):
        self.closed = False
        
        self.__connect(type, params, ifFail)
        
        self.defcursor  = self.cursor()

    def __connect(self, type, params, ifFail):
        try:
            if   type == 'postgress':
                self.connect =  psycopg2.connect(**params)
            elif type == 'oracle':
                self.connect = cx_Oracle.connect(**params)
            elif type == 'sqlite':
                self.connect =  sqlite3.connect(**params)
            elif type == 'mysql':
                self.connect =  pymysql.connect(**params)
            else:
                raise Exception('unknown db type')        
        except Exception as e:
            if ifFail:
                self.__connect(**ifFail(), ifFail=None)
            else:
                raise e
        
    
    def __getattr__(self, name):
        return getattr(self.defcursor, name)
    
    def cursor(self, *args, **params):
        return self.connect.cursor(*args, **params)
            
    def close(self):
        if not self.closed:
            self.connect.close()
            self.closed = True
    
    def __del__(self):
        #print('close db')
        self.close()
    
    def __enter__(self):
        #print('enter')
        return self
    
    def commit(self):
        self.connect.commit()
    
    def rollback(self):
        self.connect.rollback()
    
    def __exit__(self, exc_type, exc_value, traceback):
        #print('exit')
        self.close()
        
    def pprint(self, cursor=None, count=None, poleWidth=20, file=sys.stdout):
      if cursor is None:
        cursor = self.defcursor
      print(*[f'{d[0]:^{poleWidth}}' for d in cursor.description], sep='|', file=file)
      print(*(['=' * poleWidth] * len(cursor.description)) , sep='X',  file=file)
      if count is not None:
          rows = cursor.fetchmany(count)
      else:
          rows = cursor.fetchall()
      for row in rows:
        print(*[f'{str(value):^{poleWidth}}' for value in row], sep='|', file=file)
      print(f'{len(rows)} row(s)')
    
    def __call__(self, *args, **params):
        return self.execute(*args, **params)
    
    def __iter__(self):
        return self
    def __next__(self):
        buff = self.fetchone()
        if buff is not None:
            return buff
        else:
            raise StopIteration



