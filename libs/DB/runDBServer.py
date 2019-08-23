#этот фэйл у всех по идее свой
import subprocess as sp
import json


connect ={ 'type'   : 'mysql'
         , 'params' : { 'host'       : 'localhost'
                      , 'port'       : 3306
                      , 'user'       : 'root'
                      , 'password'   : ''
                      , 'db'         : 'test'
                      , 'charset'    : 'utf8'
                      , 'autocommit' : True
                      }
         }
          
cmdstart = r'E:\xampp\mysql_start.bat'

def run():
    sp.Popen([cmdstart], creationflags=sp.CREATE_NO_WINDOW)
    with open('connect.json', 'w', encoding='utf8') as fp:
        json.dump(connect, fp=fp)
        
if __name__ == '__main__':
    run()
