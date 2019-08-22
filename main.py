import os
import time

import requests as req

from bs4 import BeautifulSoup
from datetime import datetime
from DB import DB

class historical(DB):
    def __init__(self, path = r'./.db'):
        super().__init__(type='sqlite', _meta={'database' : path}, commitOnClose = True)
        self.execute("""
SELECT type, name
FROM sqlite_master
WHERE type != 'index'
""")
        poleWidth = 20
        print(*[f'{i[0]:^{poleWidth}}' for i in self.description()], f'{"cnt":^{poleWidth}}', sep=' | ')
        print("=" * poleWidth * (len(self.description()) + 1)) 
        tables = set()

        tablist = self.fetchall()
        
        for t, n, *trash in tablist:
            self.execute(f"""SELECT count(*) FROM {n}""")
            print(*[f'{i:^{poleWidth}}' for i in [t, n, self.fetchone()[0]]], sep=' | ')
            tables.add(n)
            
        print(len(tablist), 'row(s)')
        if 'log' not in tables:
            print('log alarm')
            self.execute("create table log (clock DATETIME DEFAULT (datetime('now')), ID INTEGER PRIMARY KEY AUTOINCREMENT, value BLOB)")
        
        if 'history' not in tables:
            print('history alarm')
            self.execute("""
CREATE TABLE history
( ID        varchar(10)   UNIQUE
, status    INTEGER              DEFAULT -1
, lang      varchar(100)         DEFAULT null
, reason    varchar(1000)        DEFAULT null
, read_time DATETIME             DEFAULT (datetime('now')))
)
""")
            self.readed('0' * 8, 404)
    def readed(self, ID, status = None, lang = None, reason = None):
        self("INSERT INTO history (ID, status, lang, reason) VALUES (?, ?, ?, ?)", (ID, status, lang, reason))
        self.commit()

    def log(self, *values):
        self("INSERT INTO log (value) VALUES (?)", (' '.join(map(str, values)), ))
        self.commit()
        print(f'{self.defcursor.lastrowid} : {datetime.now().strftime("%d-%m-%Y %H:%M:%S")})', *values)

    def sleep(self, mins, reason = None):
        self.log('sleep {mins} mins' + (f'reason: {reason}' if reason else ''))
        time.sleep(mins * 60)

    def operate(self, id):
        ok = False
        status = None
        while not ok:
                self.log('req ', id)
                try:
                    r = req.get(r'https://pastebin.com/' + id)
                    

                    status = r.status_code
                    
                    self.log('resp', id, status, r.reason)
                    if (status // 100 == 4 and r.reason == 'Forbidden'):
                        self.log('someone has been banned')
                        self.sleep(mins=10, reason=f'[{status} {r.reason}]')
                    elif status // 100 == 4:
                        self.readed(id, status=status, reason=r.reason)
                        ok = True
                    elif status == 503:
                        self.sleep(mins=1, reason=f'[{status} {r.reason}]')
                    elif status // 100 != 2:
                        self.log(f'strange code {id} {status} {r.reason}')
                        raise Exception(f'strange code {r.status_code}')
                    else:
                        try:
                            soup = BeautifulSoup(r.text)
                            code = soup.find('textarea', {'id': 'paste_code'}).text
                            lang = soup.find('div', {'id' : 'code_frame2'}).find('div', {'id' : 'code_buttons'}).findAll('a')[-1].text
                            with open('./parse results/' + id + '.txt', 'w', encoding='utf-8') as f:
                                print(f'lang: {lang}\n\n', file=f)
                                print(soup.find('div', {'id': 'content_left'}).find('div', {'class' : 'paste_box_frame'}), file=f)
                                print('\n\n', file=f)
                                print(code, file=f)

                            self.readed(id, status=status, lang = lang, reason=r.reason)
                            ok = True    
                        except KeyboardInterrupt as e:
                            raise e
                        except Exception as e:
                            self.sleep(mins=5, reason=e)
                except req.exceptions.ConnectionError as e:
                    self.sleep(mins=0.1, reason=e)
        return status


def cringerator(startsr):
    
    encodearr = [*[chr(i) for i in range(ord('0'), ord('9') + 1)],
                 *[chr(i) for i in range(ord('A'), ord('Z') + 1)],
                 *[chr(i) for i in range(ord('a'), ord('z') + 1)]]
                   #'0' < 'A' < 'a'

    s = [encodearr.index(litera) for litera in startsr]

    while True:
        currpos = len(startsr) - 1
        s[currpos] += 1
        while s[currpos] == len(encodearr) and currpos > 0:
            s[currpos] = 0
            currpos -= 1
            s[currpos] += 1
        #print(currpos, s)
        if s[-2] == len(encodearr):
            return
        else:
            yield  ''.join([encodearr[i] for i in s])
            
    
    return s
    #while s != [encodearr[-1]] * 8:


def run():
    with historical() as db:
        db("SELECT max(ID) FROM history")
        startid = db.fetchone()[0]
        print('start on', startid)

        if not os.path.exists('./parse results'):
            os.mkdir('./parse results')
        
        for id in cringerator(startid):
            db.operate(id)
            time.sleep(10)
                
            
if __name__ == '__main__':
    pass
    run()
    
            
