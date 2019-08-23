from . runDBServer import run
from . DB          import readJson
from . LogDB       import Loggar as DB



def runOnFail():
    run()
    return readJson(r'connect.json')

meta = readJson(path=r'connect.json', ifNotExists=runOnFail) #run


with DB(**meta, ifFail=None) as db: #runOnFail
    db("SELECT TABLE_TYPE, TABLE_NAME FROM information_schema.TABLES where TABLE_SCHEMA=%s", meta['params']['db'])
    spacing = 20
    print(*[f'{i[0]:^{spacing}}' for i in db.description], f'{"cnt":^{spacing}}', sep='|')
    print(*(['='*spacing]*(len(db.description) + 1)), sep='X')
    tables = db.fetchall()
    for i in tables:
        db(f"SELECT count(*) FROM {i[1]}")
        print(*[f'{j:^{spacing}}' for j in i], f'{db.fetchone()[0]:^{spacing}}', sep='|')
    print(f'{len(tables)} row(s)')

                
#pymysql.err.OperationalError
