import sys
import pip

def install(name, file=sys.stderr):
    global pip
    buff=sys.stdout
    
    sys.stdout=file

    if   hasattr(pip, 'main'):
        pip.main(['install', name])
    elif hasattr(pip, '_internal'):
        pip._internal.main(['install', name])
    else:
        pip = __import__('pip._internal')
        if   hasattr(pip, 'main'):
            pip.main(['install', name])
        elif hasattr(pip, '_internal'):
            pip._internal.main(['install', name])
        else:
            sys.stdout = buff
            raise ImportError('can\'t find pip.main')

    sys.stdout = buff
 

def required(name, file=sys.stderr, loadas=None, **params):
    ans = None
    try:
        ans = __import__(name,**params)
    except ImportError as e:
        print(f'{e}\n', end='', file=file)
        print('install\n', end='', file=file)
        install(loadas if loadas else name, file=file)   

        ans = __import__(name,**params)
    
    return ans

if __name__=='__main__':
    if len(sys.argv) == 2:
        help(required(sys.argv[1]))
