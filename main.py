import pymysql.cursors
from flask import Flask, render_template,request,json

connection = pymysql.connect(host='localhost',
                            user='root',
                            password='12345',
                            db='loginsys',
                            charset='utf8mb4',
                            cursorclass=pymysql.cursors.DictCursor)

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/register')
def register():
    return render_template('register.html')

@app.route('/register',methods=['POST', 'GET'])
def login():
    username=request.form['username']
    password=request.form['password']
    
    cur = connection.cursor()
    cur.execute("SELECT * from accounts WHERE username=%s AND password= %s",(username,password))
    account = cur.fetchone()
    if account:
        return "Login successful"
    else:
        return "No you cant login"

    return render_template('register.html')