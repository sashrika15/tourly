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
    return render_template('register.html')

@app.route('/register',methods=['POST', 'GET'])
def login():
    username=request.form['username']
    password=request.form['password']
    
    cur = connection.cursor()
    cur.execute("SELECT * from accounts WHERE username=%s AND password= %s",(username,password))
    account = cur.fetchone()
    if account:
        return redirect(url_for('profile'))
    else:
        return "Invalid username/password"

    return render_template('register.html')

@app.route('/profile')
def profile():
    return render_template('profile.html')

@app.route('/preference')
def preference():
    return render_template('preference.html')

@app.route('/preference',methods=['POST','GET'])
def pref():
    
    city=request.form['city']
    # if request.form.get("historic"):
    #     op1_checked = True
    #     rs+=" historic "
    # if request.form.get("architecture"):
    #     op2_checked = True
    #     rs+=" architecture "
    # if request.form.get("cultural"):
    #     op1_checked = True
    #     rs+=" cultural "
    # if request.form.get("natural"):
    #     op2_checked = True
    #     rs+=" natural "
    # if request.form.get("religion"):
    #     op1_checked = True
    #     rs+=" religion "
    # if request.form.get("sport"):
    #     op2_checked = True
    #     rs+=" sport "
    # if request.form.get("foods"):
    #     op1_checked = True
    #     rs+=" foods "
    # if request.form.get("museums"):
    #     op2_checked = True
    #     rs+=" museums "
    url = "https://api.opentripmap.com/0.1/en/places/geoname?name={}&apikey={}".format(city,api_key)
    r = requests.get(url = url)
    json_data = r.json()

    lat = json_data['lat']
    lon = json_data['lon']
    result = []

    url2="https://api.opentripmap.com/0.1/en/places/radius?radius={}&lon={}&lat={}&kinds={}&limit={}&apikey={}".format(100000,lon,lat,'historic',10,api_key)

    r1 = requests.get(url = url2)
    data = r1.json()
    feat = data['features']
    for i in feat:
        # print(i)
        prop = i['properties']
        if len(str(prop['name']))!=0:
            
            result.append(str(prop['name']))
        # result+=prop['name']+", "
        # print(result)
    
    # return "You entered result= {}".format(result)
    return redirect(url_for('dashboard',result=result,lat=lat,lon=lon))
    

@app.route('/dashboard')
def dashboard():
    result = request.args.getlist('result')

    return render_template('dashboard.html',result=result)