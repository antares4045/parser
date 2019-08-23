import os
import json
import pymysql
from runDBServer import run
from contextlib import closing





def readJson(path, ifNotExists=lambda : print('panic')):
    res = {}
    if not os.path.exists(path):
        ifNotExists()
    with open(path, 'r', encoding='utf8') as fp:
        res = json.load(fp=fp)
    return res

def runOnFail():
    run()
    return readJson(r'connect.json')

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





meta = readJson(path=r'connect.json', ifNotExists=None) #run


with DB(**meta, ifFail=None) as db: #runOnFail
    db("SELECT TABLE_TYPE, TABLE_NAME FROM information_schema.TABLES where TABLE_SCHEMA=%s", meta['params']['db'])
    spacing = 20
    print(*[f'{i[0]:^{spacing}}' for i in db.description], f'{"cnt":^{spacing}}', sep='|')
    tables = db.fetchall()
    for i in tables:
        db(f"SELECT count(*) FROM {i[1]}")
        print(*[f'{j:^{spacing}}' for j in i], f'{db.fetchone()[0]:^{spacing}}', sep='|')
    print(f'{len(tables)} row(s)')

                
#pymysql.err.OperationalError
