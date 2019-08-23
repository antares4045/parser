import sys
import json
sys.path.insert(1, '../')

from req.call import call, req

class goodProxyApi:
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
            
        respond = call(goodProxyApi.api, params={'type' : self.type, 'available' : 'yes', 'free' : 'yes', 'page' : page})
        
        
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


