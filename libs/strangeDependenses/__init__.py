import json
import sys
from required import required


def checkDependenses(taskname, encoding='utf8'):
    task = {'required' : None}
    with open(taskname, 'r', encoding=encoding) as fp:
        task = json.load(fp=fp)
    dependenses = {}
    
    for name in task['required']:
        curr = {} if task['required'][name] is None else task['required'][name]

        
        ans = required(name,
                       loadas=curr.get('loadas'))

        if curr.get('importlist'):
            for name in curr['importlist']:
                val = {} if curr['importlist'][name] is None else curr['importlist'][name]
                retname = val.get('as', name)
                dependenses[retname] = getattr(ans,name)
        else:
            dependenses[curr.get('as', name)] = ans

        

    return dependenses

if __name__ == '__main__':
    print('cheking dependences...')
    taskname = sys.argv[1] if len(sys.argv) > 1 else r'./requiredTask.json'
    encoding = 'utf8'

    
    dependenses = checkDependenses(taskname=taskname,
                                   encoding=encoding)
    
    for name in dependenses:
        print(name, ':' , dependenses[name])
