from flask import Flask, render_template, request, redirect, url_for, session
from flask_mysqldb import MySQL
import MySQLdb.cursors
import re
from datetime import timedelta


app = Flask(__name__)

app.secret_key = '001'

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'ikairakli_777'
app.config['MYSQL_DB'] = 'pythonlogin'

mysql = MySQL(app)

# 127.0.0.1/:5000/pythinlogin/home


@app.route('/pythonlogin/home')
def home():
    if 'loggedin' in session:
        return render_template('MainPage.html', username=session['username'])
    return redirect(url_for('login'))

# 127.0.0.1:5000/pythinlogin/register


@app.route('/pythonlogin/register', methods=['GET', 'POST'])
def register():

    msg = ''

    if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'email' in request.form:

        username = request.form['username']
        password = request.form['password']
        email = request.form['email']

        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM accounts WHERE username = %s', (username,))
        account = cursor.fetchone()

        if account:
            msg = 'Account already exists! / ანგარიში უკვე არსებობს!'

        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            msg = 'Invalid email address! / არასწორი მეილი!'

        elif not re.match(r'[A-Za-z0-9]+', username):
            msg = 'Username must contain only characters and numbers! / ' \
                  'მომხმარებლის სახელი უნდა შეიცავდეს მხოლოდ ასოებს და ციფრებს'

        elif not username or not password or not email:
            msg = 'Please fill out the form!/გთხოვთ შეავსოთ ყველა ველი!'

        else:
            cursor.execute('INSERT INTO accounts VALUES (NULL, %s, %s, %s)', (username, password, email,))
            mysql.connection.commit()
            msg = 'You have successfully registered! / რეგისტრაცია წარმატებით დასრულდა!'
    elif request.method == 'POST':
        msg = 'Please fill out the form! / გთხოვთ შეავსოთ ყველა ველი!'
    return render_template('register.html', msg=msg)

# 127.0.0.1:5000/pythonlogin/
@app.route('/pythonlogin/', methods=['GET', 'POST'])
def login():
    msg = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:

        username = request.form['username']
        password = request.form['password']

        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM accounts WHERE username = %s AND password = %s', (username, password,))
        account = cursor.fetchone()

        if account:
            session['loggedin'] = True
            session['id'] = account['id']
            session['username'] = account['username']
            return redirect(url_for('home'))

        else:
            msg = 'Incorrect username/password! /' \
                  ' არასწორი მომხმარებლის სახელი ან პაროლი!!'
    return render_template('index.html', msg=msg)


# 127.0.0.1:5000/python/logout
@app.route('/pythonlogin/logout')
def logout():

   session.pop('loggedin', None)
   session.pop('id', None)
   session.pop('username', None)
   return redirect(url_for('login'))

# 127.0.0.1:5000/pythinlogin/profile
@app.route('/pythonlogin/profile')
def profile():
    if 'loggedin' in session:
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM accounts WHERE id = %s', (session['id'],))
        account = cursor.fetchone()
        return render_template('profile.html', account=account)
    return redirect(url_for('login'))


app.permanent_session_lifetime = timedelta(minutes=2)
