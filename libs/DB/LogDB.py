from . DB import DB
import sys
from datetime import datetime

class Loggar(DB):
    def __init__(self, **params):
        super().__init__(**params)

        self("SELECT TABLE_NAME FROM information_schema.TABLES where TABLE_SCHEMA=%s AND TABLE_NAME='log'", (params['params']['db'],))

        if not self.fetchone():
            print('create log table')
            self('CREATE TABLE log (id int PRIMARY KEY AUTO_INCREMENT, clock DATETIME DEFAULT CURRENT_TIMESTAMP, value blob)')

        self("SELECT TABLE_NAME FROM information_schema.TABLES where TABLE_SCHEMA=%s AND TABLE_NAME=%s", (params['params']['db'], 'managers_state'))
        if not self.fetchone():
            self.log('create table', 'managers_state')
            self(f"""
CREATE TABLE managers_state
( date_update   DATETIME DEFAULT       CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
, raw           blob                   DEFAULT null
, name          varchar(100)    UNIQUE
, state         char                   DEFAULT null
)
""")

    def log(self, *values, file=sys.stdout):
        value = ' '.join(values)
        self('INSERT INTO log (value) VALUES (%s)', (value,))
        print(f'{self.lastrowid}.\t{datetime.now().strftime("%d-%m-%Y %H:%M:%S")})\t{value}\n', end='', file=file)
        
