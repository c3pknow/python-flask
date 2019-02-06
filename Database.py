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
    
    def add_article(self, title, body, author):
        try:
            self.cur.execute("INSERT INTO articles(title, body, author) VALUES(%s, %s, %s)", (title, body, author))
            self.con.commit()
        except:
            print("ERROR!!!!!!!!!!!!!!!!!!!")

    def edit_article(self, id, title, body):
        try:
            self.cur.execute("UPDATE articles SET title=%s, body=%s WHERE id=%s", (title, body, id))
            self.con.commit()
        except:
            print(f"ERROR Updating article {id}!!!!!!!!!!!!!!!!!!!")

    def delete_article(self, id):
        try:
            self.cur.execute("DELETE FROM articles WHERE id=%s", (id))
            self.con.commit()
        except:
            print(f"ERROR Deleting article {id}!!!!!!!!!!!!!!!!!!!")
        
    def get_articles(self):
        result = self.cur.execute('SELECT * FROM articles')
        articles = self.cur.fetchall()

        return articles

    def get_article(self, id):
        result = self.cur.execute('SELECT * FROM articles WHERE id = %s', [id])
        article = self.cur.fetchone()

        return article