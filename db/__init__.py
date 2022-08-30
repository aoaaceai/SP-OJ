import sqlite3
import bcrypt
from contextlib import contextmanager
import config.db as config

# The database should have the following columns:
# - uid
# - password (hashed with bcrypt)
# - role: admin / user

@contextmanager
def UserDB():
    con = sqlite3.connect(config.userDBPath)
    try:
        yield con
    finally:
        con.close()