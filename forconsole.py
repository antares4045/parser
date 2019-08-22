import os
import time
import sys
from datetime import datetime

from main import historical
from required import required
from threading import Thread

BeautifulSoup   = required('bs4').BeautifulSoup
PyQt5           = required('PyQt5')

from PyQt5.QtWidgets import QApplication, QWidget, QLabel


def newCringeratorsc(encodearr=[*[chr(i) for i in range(ord('0'), ord('9') + 1)],
                                *[chr(i) for i in range(ord('A'), ord('Z') + 1)],
                                *[chr(i) for i in range(ord('a'), ord('z') + 1)]]
                     ):
    base = len(encodearr)
    
    decoder = {encodearr[i] : i for i in range(base)}

    def decode(s):
        ans = 0
        for litera in s:
            ans *= base
            ans += decoder[litera]
        return ans

    def encode(val, minlen=1):
        ans = ''
        while val > 0 or len(ans) < minlen:
            ans = encodearr[val % base] + ans
            val = val // base
        return ans

    return decode, encode, base


def newRun(DB, encode, start, to, step=1): #[start, to)
    if not os.path.exists('./parse results'):
        os.mkdir('./parse results')
    print('start on', encode(start))
    for i in range(start, to, step):
        DB.operate(encodeId(i, 8))
        time.sleep(10)

def runUp(DB):
    decodeId, encodeId, base = newCringeratorsc()
    startid = DB("SELECT max(ID) FROM history").fetchone()[0]
    newRun(DB, encode=encodeId, start=decodeId(startid), to=base**8, step=1)


class Widget(QWidget):
    def __init__(self, db):
        super().__init__()
        self.db = db
        thread = Thread(target=runUp, kwargs={'DB' : db})
        thread.start()
        

if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = Widget(historical())
    w.show()
    app.exec_()

