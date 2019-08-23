import json
import sys
import pprint as postmen
from required import required

req = required('requests')


def sleep(secs, reason=None, file=sys.stderr):
    print('перепеши sleep!!!')
    delay = secs
    timer=[60, 60, 24, 365]
    formats=['s','m','h','d','y']
    for i in range(len(timer)):
        timer[i], secs = secs % timer[i], secs // timer[i]
    timer.append(secs)
    print(f'sleep {":".join([str(i)+d for i,d in zip(timer[::-1], formats[::-1]) if i])}' + (f' reason : {reason}' if reason else '') + '\n', end='', file=file)
    time.sleep(delay)
    
def call(*args, **params):
    print('перепеши call!!!')
    ok = False
    respond = None
    while not ok:
        try:
            respond = req.get(*args, **params)

            if respond.status_code == 200:
                ok = True
            elif respond.status_code == 403:
                raise BanError('')
            else:
                sleep(secs=5*60, reason=f'[{respond.status_code} {respond.reason}]', file=sys.stderr)
            
        except req.exceptions.ConnectionError as e:
            print(f'error {e}\n', end='', file=sys.stderr)
            #sleep(secs=5, reason=e, file=sys.stderr)
            raise e
    return respond

class goodHttpProxyApi:
    api = r'http://api.foxtools.ru/v2/Proxy'
    def __init__(self, type='https'):
        self.respo = None
        self.type  = type
    def nextPage(self):
        page = 1
        if self.respo is not None:
            page = self.respo["response"]["pageNumber"] + 1
            if page > self.respo["response"]["pageCount"]:
                raise StopIteration
            
        respond = call(goodHttpProxyApi.api, params={'type' : self.type, 'available' : 'yes', 'free' : 'yes', 'page' : page})
        
        
        self.respo = json.loads(respond.text)
        self.len = len(self.respo["response"]["items"])
        self.index = 0

    def __iter__(self):
        return self

    def __next__(self):
        if self.respo is None or self.index == self.len:
            self.nextPage()
        self.index += 1
        return self.respo["response"]["items"][self.index - 1]
        
    
    def __call__(self):
        try:
            return self.__next__()
        except StopIteration:
            return None

def myipchecker(params):
    r'http://ip-api.com/json/?fields=61439'

"""
if __name__ == '__main__':
    index = 0
    type = 'https'
    for proxy in goodHttpProxyApi(type=type):
        index += 1
        addr = f'{type}://{proxy["ip"]}:{proxy["port"]}'
        
        respo = req.get(r'http://ip-api.com/json/?fields=61439', proxies={'http' : addr})
        
        print(f'{index}. {addr}')
        print(addr)
        
        print(respo.text)
        
"""
