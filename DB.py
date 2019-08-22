import sqlite3


class DB:
    def __init__(self, type, _meta=None, commitOnClose=False):
        self.commitOnClose = commitOnClose
        self.closed = False
        if _meta is None:
            _meta=meta[type]
        if   type == 'postgress':
            self.connect = psycopg2.connect(**_meta)
        elif type == 'oracle':
            self.connect = cx_Oracle.connect(**_meta['params'], dsn=cx_Oracle.makedsn(**_meta['dsn']))
        elif type == 'sqlite':
            self.connect = sqlite3.connect(**_meta)
        else:
            raise 'unknown db type'
        self.defcursor  = self.cursor()
    
    #def __getattr__(self, name):
     #   return self.defcursor[name]
    
    def cursor(self, *args, **params):
        return self.connect.cursor(*args, **params)
    
    def execute(self, *args, **params):
        return self.defcursor.execute(*args, **params)
    
    def fetchall(self):
        return self.defcursor.fetchall()
    
    def fetchone(self):
        return self.defcursor.fetchone()

    def description(self):
        return self.defcursor.description
    
    def close(self):
        if not self.closed:
            if self.commitOnClose:
                self.commit()
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



