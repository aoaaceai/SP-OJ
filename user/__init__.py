import bcrypt
import db

class User:
    def __init__(self, uid: str, password: bytes, role: str):
        self.uid = uid
        self.password = password
        self.role = role

    def checkPassword(self, password: str):
        return bcrypt.checkpw(password.encode(), self.password)

    @property
    def isAdmin(self):
        return self.role == 'admin'

    def __repr__(self):
        return f'uid: {self.uid}, role: {self.role}'


def getUser(uid: str):
    with db.UserDB() as con:
        result = con.execute('SELECT uid, password, role FROM users WHERE uid=? LIMIT 1', (uid,)).fetchone()

        if result:
            return User(result[0], result[1].encode(), result[2])
        else:
            return None

def verify(uid: str, password: str):
    user = getUser(uid)
    if not user:
        return False
    return user.checkPassword(password)
