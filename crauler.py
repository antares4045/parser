import json
import time
import sys

from required import required

fake_useragent = required('fake_useragent')
req            = required('requests')
#BeautifulSoup  = required('bs4').BeautifulSoup



class BanError(BaseException):
    def __init__(self, m='ban error'):
        self.message = m
    def __str__(self):
        return self.message
"""
    def __init__(self, *args):
        super().__init__(*args)
"""


#print(header)

def sleep(secs, reason=None, file=sys.stderr):
    delay = secs
    timer=[60, 60, 24, 365]
    formats=['s','m','h','d','y']
    for i in range(len(timer)):
        timer[i], secs = secs % timer[i], secs // timer[i]
    timer.append(secs)
    print(f'sleep {":".join([str(i)+d for i,d in zip(timer[::-1], formats[::-1]) if i])}' + (f' reason : {reason}' if reason else '') + '\n', end='', file=file)
    time.sleep(delay)



def call(*args, **params):
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
    def __init__(self):
        self.respo = None
        
    def nextPage(self):
        page = 1
        if self.respo is not None:
            page = self.respo["response"]["pageNumber"] + 1
            if page > self.respo["response"]["pageCount"]:
                raise StopIteration
            
        respond = call(goodHttpProxyApi.api, params={'type' : 'http', 'available' : 'yes', 'free' : 'yes', 'page' : page})
        
        
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
        
        #http://api.foxtools.ru/v2/Proxy?type=http&available=yes&free=yes?page=1
        
        
        

def getHttpsProxy(params = {}):
    ok = False
    ans = None
    reqlist = [(r'https://api.getproxylist.com/proxy?allowsHttps=1', lambda respond: json.loads(respond.text)),
               (r'http://pubproxy.com/api/proxy?https=true&format=json', lambda respond: json.loads(respond.text)["data"][0])
                ]
    for request, scrap in  reqlist: 
        try:
            respond = call(request, **params)
            ans = scrap(respond)
            return ans
        except BanError:
            print(f'ban on {request}\n', end='', file=sys.stderr)
    
    raise BanError('today not redy to find another proxy')
    
    

if __name__ == '__main__':
    if False:
        ok = False
        while not ok:
            try:
                headers = {'accept' : 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng',
                                      'accept-encoding': 'gzip, deflate, br',
                                      'accept-language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
                                      'user-agent' : fake_useragent.UserAgent().random}

                print('getting proxy')
                #httpsProxy = getHttpsProxy()
                #print(httpsProxy)
                #proxy = {'https' : f'https://{httpsProxy["ip"]}:{httpsProxy["port"]}'} #{"https": "https://182.52.90.43:33326"}, {'https': 'https://82.114.241.138:8080'} 

                proxy = {'https' : r'https://nl-132-134-226.fri-gate0.org:443'}

                params = {'proxies' : proxy, 'headers' : headers}
                print(json.dumps(params))

                respond = req.get(r'https://pastebin.com/N86DD84w', **params)

                
                print(f'[{respond.status_code} {respond.reason}]')
                if respond.status_code == 200:
                    print(respond.text)

                    ok=True
                
            except req.exceptions.ConnectionError as e:
                print(f'error {e}\n', end='', file=sys.stderr)
                ok = False
    else:
        index = 0
        for httpsProxy in goodHttpProxyApi():
            index += 1
            print(index, f'https://{httpsProxy["ip"]}:{httpsProxy["port"]}')
