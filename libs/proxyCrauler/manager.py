import sys
sys.path.insert(1, '../')

from DB import DB, meta
if __name__ == '__main__':
    print('\n\nprocesslist:')
    with DB(**meta) as ff:
        ff('SELECT ID,STATE,STAGE,COMMAND,INFO FROM information_schema.processlist')
        ff.pprint()
