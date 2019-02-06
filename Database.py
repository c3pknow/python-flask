import pymysql

class Database:
    def __init__(self):
        host = 'localhost'
        user = 'root'
        password = ''
        db = 'flaskapp'

        self.con = pymysql.connect(host=host, user=user, password=password, db=db, cursorclass=pymysql.cursors.DictCursor)
        self.cur = self.con.cursor()

    def register_user(self, name, email, username, password):
        try:
            self.cur.execute("INSERT INTO users(name, email, username, password) VALUES(%s, %s, %s, %s)", (name, email, username, password))
            self.con.commit()
        except:
            print("ERROR!!!!!!!!!!!!!!!!!!!")
        
    def get_user_by_username(self, username):
        result = self.cur.execute('SELECT * FROM users WHERE username = %s', [username])

        if result > 0:
            return self.cur.fetchone()
            