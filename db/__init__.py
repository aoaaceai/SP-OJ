import sqlite3
from os.path import dirname
import bcrypt
from contextlib import contextmanager

@contextmanager
def DBConn():
    con = sqlite3.connect(dirname(__file__) + '/users.db')
    try:
        yield con
    finally:
        con.close()


def checkPassword(uid: str, password: str):
    with DBConn() as con:
        result = con.cursor().execute('SELECT password FROM users WHERE uid=? LIMIT 1', (uid,)).fetchone()

        if not result:
            return False
        else:
            result = result[0].encode()

        result = bcrypt.checkpw(password.encode(), result)
        return result
