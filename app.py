from flask import Flask, render_template, request, redirect
from flask_mysqldb import MySQL
import yaml

app = Flask(__name__)

db = yaml.load(open('db.yaml'))
app.config['MYSQL_HOST'] = db['mysql_host']
app.config['MYSQL_USER'] = db['mysql_user']
app.config['MYSQL_PASSWORD'] = db['mysql_password']
app.config['MYSQL_DB'] = db['mysql_db']

mysql = MySQL(app)

@app.route('/', methods=['GET', 'POST'])
def index():
  if request.method == 'POST':
    username = request.form['username']
    password = request.form['password']
    cursor = mysql.connection.cursor()
    data = cursor.execute(f"SELECT * FROM Users WHERE (username='{username}');")
    if data:
      user = cursor.fetchone()
      cursor.close()
    if password == user[2]:
      return 'Success'
    return redirect('/')
  else:
    return render_template('index.html')

if __name__ == '__main__':
  app.run(debug=True)