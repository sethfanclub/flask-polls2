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
  cursor = mysql.connection.cursor()
  cursor.execute("SELECT * FROM Questions;")
  polls = cursor.fetchall()
  return render_template('index.html', polls=polls)

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
    try:
      cursor.execute("INSERT INTO Users (username, email, password) VALUES (%s, %s, %s)",(username, email, hashed_password))
      cursor.execute(f"SELECT * FROM Users WHERE (username='{username}');")
      user = cursor.fetchone()
      mysql.connection.commit()
    except:
      return 'Database returned an error'
    cursor.close()
    session['user'] = user
    return redirect('/')

  else:
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
  if g.user:
    return redirect('/')
  if request.method == 'POST':
    username = request.form['username']
    password = request.form['password']
    cursor = mysql.connection.cursor()
    try:
      cursor.execute(f"SELECT * FROM Users WHERE (username='{username}');")
      user = cursor.fetchone()
    except:
      return 'User not found'
    cursor.close()
    if bcrypt.checkpw(password.encode('utf-8'), user[2].encode('utf-8')):
      session['user'] = user
      return redirect('/')
    else:
      return 'Incorrect password'
  else:
    return render_template('login.html')

@app.route('/logout')
def logout():
  if g.user:
    session.pop('user', None)
  return redirect('/')

@app.route('/create-poll', methods=['GET', 'POST'])
def create_poll():
  if not g.user:
    return redirect('/')
  if request.method == 'POST':
    question = request.form['question']
    choice1 = request.form['choice1']
    choice2 = request.form['choice2']
    cursor = mysql.connection.cursor()
    try:
      cursor.execute(f"INSERT INTO Questions (content) VALUES ('{question}');")
      cursor.execute(f"SELECT id FROM Questions WHERE (content='{question}');")
      question_id = cursor.fetchone()[0]
      cursor.execute(f"INSERT INTO Choices (question_id, content) VALUES ('{question_id}', '{choice1}');")
      cursor.execute(f"INSERT INTO Choices (question_id, content) VALUES ('{question_id}', '{choice2}');")
      mysql.connection.commit()
    except:
      return 'Database returned an error'
    cursor.close()

    return redirect('/')
  else:  
    return render_template('create_poll.html')

@app.before_request
def before_request():
  g.user = None

  if 'user' in session:
    g.user = session['user']

if __name__ == '__main__':
  app.run(debug=True)

# POLL VOTING PAGE AND POLL AUTHORS