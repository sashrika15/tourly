import pymysql.cursors
from flask import Flask, render_template,request,json,redirect,url_for,session
import requests
import json
import sqlite3

app = Flask(__name__)
app.secret_key = 'a random string'
api_key = "5ae2e3f221c38a28845f05b674ad5fbdc89d5d4039b07c283619ac27"


@app.route('/')
def home():
    session['res']={}
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

    connection = sqlite3.connect('./data/loginsys.db')
    cur = connection.cursor()
    query="SELECT * from accounts WHERE username='{}' AND password= '{}'".format(username,password)
    cur.execute(query)
    account = cur.fetchone()
    if account:
        return redirect(url_for('profile',name=username))
    else:
        return "Invalid username/password"
    connection.close()

    return render_template('register.html')

@app.route('/register/newuser')
def newuser():
    return render_template('newuser.html')

@app.route('/register/newuser',methods=['POST', 'GET'])
def createaccount():
    username=request.form['username']
    password=request.form['password']
    connection = sqlite3.connect('./data/loginsys.db')
    cur = connection.cursor()
    query = "INSERT INTO accounts VALUES ('{}','{}');".format(username,password)
    cur.execute(query)
    connection.commit()
    connection.close()
    return redirect(url_for('register',message='New user created! Please login'))

@app.route('/profile')
def profile():
    if request.args.get('name'):
        name = request.args.get('name')
    else:
        name="Jane Doe"
    return render_template('profile.html',name=name)

@app.route('/preference')
def preference():
    return render_template('preference.html')

@app.route('/preference',methods=['POST','GET'])
def pref():
    session['res'] = {}
    rs=""
    city=request.form['city']
    stops=request.form['stops']
    radius=request.form['radius']
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
    res={}
    xiddict={}
    
    lat = json_data['lat']
    lon = json_data['lon']

    # url4="https://api.opentripmap.com/0.1/en/places/xid/{}?apikey=5ae2e3f221c38a28845f05b674ad5fbdc89d5d4039b07c283619ac27".format(xid)

    url2="https://api.opentripmap.com/0.1/en/places/radius?radius={}&lon={}&lat={}&kinds={}&rate=1&limit={}&apikey={}".format(radius,lon,lat,rs,stops,api_key)

    r1 = requests.get(url = url2)
    data = r1.json()
    feat = data['features']
    for i in feat:
        prop = i['properties']
        geo = i['geometry']
        
        if len(str(prop['name']))!=0:
            res[str(prop['name'])]=geo['coordinates']
            xiddict[str(prop['name'])]=prop['xid']

    # print(xiddict)
    
    session['res'] = res
    session['xiddict'] = xiddict

    return redirect(url_for('dashboard',city=city,result=res,lat=lat,lon=lon,msg="Here are your recommended tourist spots!"))
    

@app.route('/dashboard')
def dashboard():

    result = session['res']
    
    if request.args.get('city'):
        city = request.args.get('city')
    else:
        city="India"

    if request.args.get('msg'):
        msg = request.args.get('msg')
        zoom=12
    else:
        msg = "Welcome to the Dashboard! "
        zoom=3

    if request.args.get('lat'):
        lat = request.args.get('lat')
    else:
        lat = 22.998851594142913
        

    if request.args.get('lon'):
        lon = request.args.get('lon')
    else:
        lon = 78.22265625

    return render_template('dashboard.html',result=result,msg=msg,lat=lat,lon=lon,city=city,zoom=zoom)

@app.route('/map')
def map():
    return render_template('map.html')