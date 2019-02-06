from flask import Flask, request, render_template, flash, redirect, url_for, session, logging
from data import Articles
from wtforms import Form, StringField, TextAreaField, PasswordField, validators
# from flaskext.mysql import MySQL
from passlib.hash import sha256_crypt
from Database import Database
from functools import wraps


app = Flask(__name__)
app.debug = True

# Config MySQL
db = Database()

# Initialize MySQL
#mysql = MySQL(app)

Articles = Articles()

@app.route('/')
def index():
    return render_template('home.htm')

@app.route('/about')
def about():
    return render_template('about.htm')

@app.route('/articles')
def articles():
    return render_template('articles.htm', articles = Articles)

@app.route('/articles/<string:id>/')
def article(id):
    return render_template('article.htm', id=id)




class RegisterForm(Form):
    name = StringField('Name', [validators.Length(min=1, max=50)])
    username = StringField('Username', [validators.Length(min=4, max=25)])
    email = StringField('Email', [validators.Length(min=6, max=50)])
    password = PasswordField('Password', [
        validators.DataRequired(),
        validators.EqualTo('confirm', message='Passwords do not match')
    ])
    confirm = PasswordField('Confirm Password')

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm(request.form)

    if request.method == 'POST' and form.validate():
        name = form.name.data
        email = form.email.data
        username = form.username.data
        password = sha256_crypt.encrypt(str(form.password.data))

        db.register_user(name, email, username, password)
        flash('You are now registered and can log in', 'success')

        return redirect(url_for('login'))

    return render_template('register.htm', form=form)


# User Login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password_candidate = request.form['password']

        result = db.get_user_by_username(username)

        if result is None:
            app.logger.info('Login: No user record found')
            error = 'Username not found'
            return render_template('login.htm', error=error)
        else:
            password = result['password']

            if sha256_crypt.verify(password_candidate, password):
                app.logger.info('Login: Password matched')

                session['is_logged_in'] = True
                session['username'] = username
                flash('You are now logged in', 'success')
            
                return redirect(url_for('dashboard'))
            else:
                error = 'The username and password entered are incorrect.  Please try again.'
                return render_template('login.htm', error=error)


    return render_template('login.htm')


def is_logged_in(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'is_logged_in' in session:
            return f(*args, **kwargs)
        else:
            flash('Unauthorized, please log in', 'danger')
            return redirect(url_for('login'))
    return wrap



@app.route('/dashboard')
@is_logged_in
def dashboard():
    return render_template('dashboard.htm')


@app.route('/logout')
def logout():
    session.clear()
    flash('You are now logged out', 'success')
    return redirect(url_for('login'))



if __name__ == '__main__':
    app.secret_key = 'secret1234567654321'
    app.run()