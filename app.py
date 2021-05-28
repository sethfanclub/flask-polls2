from flask import Flask, render_template, request, redirect, session, g
from flask_mysqldb import MySQL
import yaml
import bcrypt
import os


db = yaml.load(open('db.yaml'))

app = Flask(__name__)
app.secret_key = os.urandom(24)
app.config['MYSQL_HOST'] = db['mysql_host']
app.config['MYSQL_USER'] = db['mysql_user']
app.config['MYSQL_PASSWORD'] = db['mysql_password']
app.config['MYSQL_DB'] = db['mysql_db']

mysql = MySQL(app)

@app.route('/')
def index():
  return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
  if g.user:
    return redirect('/')
  if request.method == 'POST':
    username = request.form['username']
    email = request.form['email']
    if request.form['password1'] == request.form['password2']:
      password = request.form['password2']
      hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    else:
      return "Passwords didn't match"
    
    cursor = mysql.connection.cursor()
    cursor.execute("INSERT INTO Users (username, email, password) VALUES (%s, %s, %s)",(username, email, hashed_password))
    data = cursor.execute(f"SELECT * FROM Users WHERE (username='{username}');")
    if data:
      user = cursor.fetchall()[0]
    mysql.connection.commit()
    cursor.close()
    session['user'] = user
    return redirect('/')

  else:
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
  if request.method == 'POST':
    pass
  else:
    return render_template('login.html')

@app.before_request
def before_request():
  g.user = None

  if 'user' in session:
    g.user = session['user']

if __name__ == '__main__':
  app.run(debug=True)