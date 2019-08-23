import sys
import json

from datetime import datetime
sys.path.insert(1, '../')

from DB import DB, meta

from goodApi import goodProxyApi




class Manager(DB):
    def __init__(self, name='proxyScrapData', meta=meta):
        super().__init__(**meta)

        self.schema = meta['params']['db']
        self.name  = name
        self("SELECT TABLE_NAME FROM information_schema.TABLES where TABLE_SCHEMA=%s AND TABLE_NAME=%s", (self.schema, self.name))
        if not self.fetchone():
            self.log('create table', self.name)
            self(f"""
CREATE TABLE {self.name}
( date_create   DATETIME DEFAULT   CURRENT_TIMESTAMP
, date_update   DATETIME DEFAULT   CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
, raw           blob
, socket        varchar(100)       UNIQUE
, hugeAnonimity char     DEFAULT 'N'
)
""")
        self('SELECT * FROM managers_state WHERE name=%s', (self.name,))

        row = self.fetchone()
        
        if not row:
            self("INSERT INTO managers_state (name) VALUES (%s)", (self.name,))
            self.scan()
        elif (datetime.now() - row[0]).seconds > 3600:
            self.scan()
        
    def scan(self, type='https'):
        self("UPDATE  managers_state SET date_update=CURRENT_TIMESTAMP WHERE name=%s",  (self.name,))
        for proxy in goodProxyApi(type=type):
            socket = f'{type}://{proxy["ip"]}:{proxy["port"]}'
            self(f"SELECT * from {self.name} where socket=%s", (socket,))

            sql = ''
            
            if self.fetchone():
                self.log('update socket', socket)
                sql = f"UPDATE {self.name} SET raw=%s where socket=%s"
            else:
                self.log('learn socket', socket)
                sql = f'INSERT INTO {self.name} (raw, socket) VALUES (%s, %s)'
                     
            self(sql, (json.dumps(proxy), socket))
            
            
        

            
        


if __name__ == '__main__':
    
    with Manager(name='proxyScrapData') as ff:
        ff('SELECT ID,STATE,STAGE,COMMAND,INFO FROM information_schema.processlist')
        print('\n\nprocesslist:')
        ff.pprint()
