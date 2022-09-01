import db
from problem import getProblem, getProblems
from threading import Thread, current_thread, main_thread
from datetime import datetime, timedelta
from time import sleep

def useQuota(pid: int, uid: str):
    problem = getProblem(pid)

    if not problem:
        return False

    with db.QuotaDB() as con:
        result = con.execute('SELECT quota FROM quotas WHERE pid=? AND uid=?', (pid, uid)).fetchone()
        if result:
            quota = result[0]
            if quota <= 0:
                return False
            con.execute('UPDATE quotas SET quota=? WHERE pid=? AND uid=?', (quota-1, pid, uid))
            con.commit()
            return True
        elif problem.quota >= 1:
            con.execute('INSERT INTO quotas VALUES (?, ?, ?)', (pid, uid, problem.quota-1))
            con.commit()
            return True
        else:
            con.execute('INSERT INTO quotas VALUES (?, ?, ?)', (pid, uid, 0))
            con.commit()
            return False

def resetQuota(pid: int, uid: str):
    problem = getProblem(pid)

    if not problem:
        return False

    with db.QuotaDB() as con:
        if con.execute('SELECT quota FROM quotas WHERE pid=? AND uid=?', (pid, uid)).fetchone():
            con.execute('UPDATE quotas SET quota=? WHERE pid=? AND uid=?', (pid, uid))
        else:
            con.execute('INSERT INTO quotas VALUES (?, ?, ?)', (pid, uid, problem.quota))
        
        con.commit()
        return True

def resetQuotas():
    print('Resetting quotas...')
    problems = getProblems()

    with db.QuotaDB() as con:
        for problem in problems:
            con.execute('UPDATE quotas SET quota=? WHERE pid=?', (problem.quota, problem.id))

        con.commit()

def getQuota(pid: int, uid: int):
    problem = getProblem(pid)

    if not problem:
        return 0

    with db.QuotaDB() as con:
        result = con.execute('SELECT quota FROM quotas WHERE pid=? AND uid=?', (pid, uid)).fetchone()
        if result:
            return result[0]
        else:
            con.execute('INSERT INTO quotas VALUES (?, ?, ?)', (pid, uid, problem.quota))
            con.commit()
            return problem.quota

def resetQuotasPeriodically():
    def sleepUntil(t: datetime):
        sleep((t-datetime.now()).total_seconds())

    def tomorrow():
        today = datetime.today()
        return datetime(today.year, today.month, today.day) + timedelta(days=1)

    def child():
        while True:
            sleepUntil(tomorrow())
            resetQuotas()

    if current_thread() is main_thread():
        Thread(target=child, daemon=True).start()

resetQuotasPeriodically()