import sqlite3
import bcrypt
from contextlib import contextmanager
import config.db as config

@contextmanager
def DBConn(path):
    con = sqlite3.connect(path)
    try:
        yield con
    finally:
        con.close()


def checkPassword(uid: str, password: str):
    with DBConn(config.userDBPath) as con:
        result = con.cursor().execute('SELECT password FROM users WHERE uid=? LIMIT 1', (uid,)).fetchone()

        if not result:
            return False
        else:
            result = result[0].encode()

        result = bcrypt.checkpw(password.encode(), result)
        return result
