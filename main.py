from flask import Flask
import os 
from flask import Flask, flash, redirect, render_template, request, session, abort
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import sessionmaker
from tabledefinition import *

engine = create_engine('sqlite:///users.db', echo=True)
app = Flask(__name__)

NEW_USERNAME = ''
NEW_PASSWORD = ''


@app.route('/', methods=['GET', 'POST'])
def home():
    global NEW_USERNAME
    
    #---------------------------------------
    
    
    if not session.get('logged_in'):
        return render_template('index.html')
    else:
        global NEW_USERNAME
        return render_template('signedin.html', NEW_USERNAME=NEW_USERNAME)
    
    return render_template('index.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        global NEW_USERNAME
        global NEW_PASSWORD
        NEW_USERNAME = str(request.form['NEW_USERNAME'])
        NEW_PASSWORD = str(request.form['NEW_PASSWORD'])
        EMAILADDRESS = str(request.form['EMAILADDRESS'])
        bio = str(request.form['bio'])
        dob = str(request.form['dob'])
        # create a Session
        Session = sessionmaker(bind=engine)
        s = Session()


        user = User(NEW_USERNAME,NEW_PASSWORD,EMAILADDRESS, bio, dob)
        s.add(user)

        s.commit()
        session['logged_in'] = True
        return home()
    
    return render_template('signup.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':

        global NEW_USERNAME
        global NEW_PASSWORD
        NEW_USERNAME = str(request.form['NEW_USERNAME'])
        NEW_PASSWORD = str(request.form['NEW_PASSWORD'])
        Session = sessionmaker(bind=engine)
        s = Session()
        query = s.query(User).filter(User.username.in_([NEW_USERNAME]), User.password.in_([NEW_PASSWORD]))
        result = query.first()
        if result:
            session['logged_in'] = True
        else:
            flash('wrong password!')
        return home()
    
    return render_template('login.html')

@app.route('/profile', methods=['GET', 'POST'])
def profile():
    if request.method == 'POST':
        return render_template('myprofile.html')
    else:  
        return render_template('myprofile.html', NEW_USERNAME = NEW_USERNAME)
    
@app.route('/feed', methods=['GET', 'POST'])
def feed():
    global NEW_USERNAME
    if request.method == 'POST':
        Session = sessionmaker(bind=engine)
        s = Session()
        userresult = s.query(User)
        return render_template('feed.html', userresult = userresult)
        
    else:
        Session = sessionmaker(bind=engine)
        s = Session()
        userresult = s.query(User)
        return render_template('feed.html', userresult = userresult)
    
@app.route('/logout', methods=['GET', 'POST'])
def logout():
    session['logged_in'] = False
    return home()

@app.route('/contactus', methods=['POST', 'GET'])
def contactus():
    return render_template('contactus.html')

if __name__ == "__main__":
    app.secret_key = os.urandom(12)
    app.run(debug=True,host='0.0.0.0', port=4000)
