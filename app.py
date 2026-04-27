
from flask import Flask, render_template, request, redirect, session
import mysql.connector
import pandas as pd
import os

app = Flask(__name__)

app.secret_key = "123"
CSV_FILE = "apple_data.csv"

# DB connection

db = mysql.connector.connect(
  host="localhost",
  user="root",
  password="Root",
  database="Apple"
)
# LOGIN

@app.route('/login', methods=['GET','POST'])

def login():

  if request.method == 'POST':
    username = request.form['Username']
    password = request.form['Password']
    cursor = db.cursor()
    cursor.execute( "SELECT * FROM users WHERE username=%s AND password=%s",(username, password))
    user = cursor.fetchone()
    if user:
      session['user'] = username
      return redirect('/')
    else:
     return "Wrong login"

  return render_template('login.html')

@app.route('/', methods=['GET','POST'])
def home():
  if 'user' not in session:
    return redirect('/login')
  if request.method == 'POST':
    name = request.form['FullName']
    password = request.form['PASSWORD']
    # SAVE TO MYSQL
    cursor = db.cursor()
    cursor.execute( "INSERT INTO students (FullName, PASSWORD) VALUES (%s,%s)",(name, password))
    db.commit()

# VIEW apple data
@app.route('/table')
def table():

  if 'user' not in session:
    return redirect('/login')
  cursor = db.cursor()
  cursor.execute("SELECT * FROM students")
  db_data = cursor.fetchall()
  if os.path.exists(CSV_FILE):
    df = pd.read_csv(CSV_FILE)
    csv_data = df.to_html()
  else:
    csv_data = "No CSV data"
  return render_template('table.html', db_data=db_data, csv_data=csv_data)
# LOGOUT
@app.route('/logout')
def logout():
  session.clear()
  return redirect('/login')

app.run(debug=True)







