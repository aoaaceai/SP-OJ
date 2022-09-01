import sqlite3
from contextlib import contextmanager
import config.db as config

# The user database should have the following columns:
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

# The quota database sholud have the following columns:
# - pid (integer)
# - uid (text)
# - quota (integer)

@contextmanager
def QuotaDB():
    con = sqlite3.connect(config.quotaDBPath)
    try:
        yield con
    finally:
        con.close()