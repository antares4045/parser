import sys
import requests as req

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
