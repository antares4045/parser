#то, что нужно для многопоточника
import sys
import subprocess as sp
from threading import Thread, Lock
#Lock скорее нужен для сэмпла, но без него врядли обойдётся

#то, что нужно для красивостей многопоточника
from datetime import datetime

#то, что нужно для сэмпла
import time
 

lockForBorders=Lock()
def f_reader(proc, id, operate=lambda value, reader: None, logBorders=False, encoding='utf8', lockForBorders=lockForBorders):
    #у дефолтного оперейта по идее в теле должен быть pass, но лямбда должна иметь значение
    if logBorders:
        lockForBorders.acquire()
        print(f'   begin  {id:^4} {datetime.now()}', file=sys.stderr)
        lockForBorders.release()

    while proc.poll() is None:
        line = proc.stdout.readline()
        if type(line) != str:
            line = line.decode(encoding)
        operate(value=line, reader=id)
        
    if logBorders:
        lockForBorders.acquire()
        print(f'endlines  {id:^4} {datetime.now()}', file=sys.stderr)
        lockForBorders.release()

    for line in proc.stdout.readlines():
        if type(line) != str:
            line = line.decode(encoding)
        operate(value=line, reader=id)
    
    if logBorders:
        lockForBorders.acquire()
        print(f'   end    {id:^4} {datetime.now()}', file=sys.stderr)
        lockForBorders.release()




stdoutLock = Lock()
def log(value, reader):
    value = value.strip()
    if value:
        value = f'{datetime.now()} {reader:^4} {value}'
        
        stdoutLock.acquire()
        print(value)
        stdoutLock.release()
    

def mapCaller():
    ENCODE = 'utf8'
    size = 10

    readers = []
    
    for i in range(size):
        proc = sp.Popen([sys.executable, '-u', sys.argv[0], str(i)], stdout=sp.PIPE, creationflags=sp.CREATE_NO_WINDOW, encoding=ENCODE)
        reader = Thread(target=f_reader, kwargs={ 'proc' : proc,
                                                  'operate' : log,
                                                  'id' : f'reader#{i}',
                                                  'logBorders' : True,
                                                  'encoding' : ENCODE ,
                                                  'lockForBorders' : stdoutLock})
        reader.start()
        readers.append(reader)

    for reader in readers:
        reader.join()
        
                    

def mapPrinter(delay):

    for i in range(3):
        print(datetime.now(), i)
        time.sleep(delay)
        print()

    print(datetime.now())
    print()
    

if __name__ == '__main__':
    #print(f'   start      {datetime.now()} {sys.argv}\n', end='') #возможно вторжение извне но не внутрь солидной строки, потому даже \n при себе

    if len(sys.argv) == 1:
        mapCaller()
    else:
        mapPrinter(int(sys.argv[1]))
    

    #print(f'   finish     {datetime.now()}\n', end='')
