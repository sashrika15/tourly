import pymysql.cursors
from flask import Flask, render_template,request,json,redirect,url_for
import requests
import json

connection = pymysql.connect(host='localhost',
                            user='root',
                            password='12345',
                            db='loginsys',
                            charset='utf8mb4',
                            cursorclass=pymysql.cursors.DictCursor)

app = Flask(__name__)
api_key = "5ae2e3f221c38a28845f05b674ad5fbdc89d5d4039b07c283619ac27"

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/register')
def register():
    if request.args.get('message'):
        msg = request.args.get('message')
    else:
        msg="Welcome!"
    return render_template('register.html',message=msg)

@app.route('/register',methods=['POST', 'GET'])
def login():
    username=request.form['username']
    password=request.form['password']
    
    cur = connection.cursor()
    cur.execute("SELECT * from accounts WHERE username=%s AND password= %s",(username,password))
    account = cur.fetchone()
    if account:
        return redirect(url_for('profile',name=username))
    else:
        return "Invalid username/password"

    return render_template('register.html')

@app.route('/register/newuser')
def newuser():
    return render_template('newuser.html')

@app.route('/register/newuser',methods=['POST', 'GET'])
def createaccount():
    username=request.form['username']
    password=request.form['password']
    
    cur = connection.cursor()
    query = "INSERT INTO accounts VALUES ('{}','{}');".format(username,password)
    cur.execute(query)
    connection.commit()
    return redirect(url_for('register',message='New user created! Please login'))

@app.route('/profile')
def profile():
    name = request.args.get('name')
    return render_template('profile.html',name=name)

@app.route('/preference')
def preference():
    return render_template('preference.html')

@app.route('/preference',methods=['POST','GET'])
def pref():
    rs=""
    city=request.form['city']
    if request.form.get("historic"):
        rs+="historic%2C"
    if request.form.get("architecture"):
        rs+="architecture%2C"
    if request.form.get("cultural"):
        rs+="cultural%2C"
    if request.form.get("natural"):
        rs+="natural%2C"
    if request.form.get("religion"):
        rs+="religion%2C"
    if request.form.get("sport"):
        rs+="sport%2C"
    if request.form.get("foods"):
        rs+="foods%2C"
    if request.form.get("museums"):
        rs+="museums%2C"
    url = "https://api.opentripmap.com/0.1/en/places/geoname?name={}&apikey={}".format(city,api_key)
    r = requests.get(url = url)
    json_data = r.json()

    lat = json_data['lat']
    lon = json_data['lon']
    result = []

    url2="https://api.opentripmap.com/0.1/en/places/radius?radius={}&lon={}&lat={}&kinds={}&limit={}&apikey={}".format(100000,lon,lat,rs,10,api_key)

    r1 = requests.get(url = url2)
    data = r1.json()
    feat = data['features']
    for i in feat:
        prop = i['properties']
        if len(str(prop['name']))!=0:
            
            result.append(str(prop['name']))
            
    return redirect(url_for('dashboard',result=result,lat=lat,lon=lon))
    

@app.route('/dashboard')
def dashboard():
    result = request.args.getlist('result')

    return render_template('dashboard.html',result=result)