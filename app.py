from flask import Flask,render_template,request,redirect,session
from db import DataBase
import api

app = Flask(__name__)
dbo = DataBase()

@app.route('/')
def index():
    return render_template('login.html')
@app.route('/register')
def register():
    return render_template('register.html')
@app.route('/perform_registration',methods =['post'])
def perform_registration():
    name = request.form.get('user_name')
    email = request.form.get('user_email')
    password = request.form.get('user_password')
    response = dbo.insert(name,email,password)
    if response:
        return render_template("login.html",message = 'Successfull Please Login Here')
    else:
        return render_template("register.html",message = 'Email Already Exists')
@app.route('/perform_login',methods = ['post'])
def perform_login():
    session['logged_in'] = 1
    email = request.form.get('user_email')
    password = request.form.get('user_password')
    response = dbo.search(email,password)
    if response:
        return redirect('/profile')
    else:
        return render_template("login.html", message='Wrong Credentials')
@app.route('/profile')
def profile():
    return render_template('profile.html')

@app.route('/ner')
def ner():
    if session:
        return render_template('ner.html')
    else:
        return redirect('/')
@app.route('/perform_ner')
def perform_ner():
    if session:
        text = request.form.get('ner_text')
        response = api.ner(text)
        print(response)

        return render_template('ner.html', response=response)
    else:
        return redirect('/')



app.run(debug = True)