from flask import Flask, render_template, request, session , g , redirect , url_for ,abort, render_template , flash, jsonify
import sqlite3
import gc
import json
#from textstat.textstat import textstat
#import re
import urllib
from passlib.hash import sha256_crypt
from functools import wraps
import modules

DATABASE = 'Banker.db'
DEBUG = True
SECRET_KEY = 'development_key'

app = Flask(__name__)
app.config.from_object(__name__)

def login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            flash("Please Login to view this page...")
            return redirect(url_for('login_page'))
    return wrap

def connect_db():
    return sqlite3.connect(app.config['DATABASE'])


@app.before_request
def before_request():
    g.db = connect_db()

@app.teardown_request
def teardown_request(exception):
    db = getattr(g,'db',None)
    if db is not None:
        db.close()
        gc.collect()

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.route('/')
def index():
    return redirect(url_for('login_page'))



@app.route('/login/', methods=["GET","POST"])
def login_page():
    try:
        if 'logged_in' in session:
            return redirect(url_for('chat_page'))
        if request.method == "POST":

            username = request.form['username']
            password = request.form['password']

            cur = g.db.execute('select username,password from userdb where username=?',[username])
            row = cur.fetchone()
            if row is None:
                flash("Invalid Login, Please try again..")
                return render_template('login.html')

            if sha256_crypt.verify(password, row[1]):
                session['logged_in'] = True
                session['username'] = username
                return redirect(url_for('chat_page'))
            else:
                flash("Invalid Login, Please try again...")
                return render_template('login.html')
        else:
            return render_template('login.html')
    except Exception as e:
        flash(e)
        flash("Invalid login, Please try again")
        return render_template('login.html')

@app.route('/logout/')
@login_required
def logout():
    session.clear()
    flash("you have been succesfully logged out")
    return redirect(url_for('index'))



@app.route('/register/',methods=['GET','POST'])
def register_page():
    try:
        if request.method == "POST":

            username = request.form['username']
            password = request.form['password']
            passconfirm = request.form['passconfirm']

            if password != passconfirm:
                flash("Passwords do not match")
                return render_template('register.html')


            cur = g.db.execute('select username from userdb where username=?',[username])

            rows = cur.fetchall()

            if len(rows) != 0 :
                flash('username already exists')
                return render_template('register.html')

            else:
                password = sha256_crypt.encrypt(request.form['password'])
                g.db.execute('insert into userdb (username,password) values(?,?)',[username,password])
                g.db.execute('insert into account (username,amount) values(?,?)',[username,1000])
                g.db.commit()
                flash("Thank you for registering, please login")
                return redirect(url_for('login_page'))
        else:
            return render_template('register.html')
    except Exception as e:
        flash(e)
        return render_template('register.html')

@app.route('/chat/',methods=['GET','POST'])
@login_required
def chat_page():
    return render_template('chat.html')

@app.route('/process/', methods=['GET','POST'])
@login_required
def process_request():
    try:
        if request.method == "GET":
            user_input = request.args.get('user_input')
            return user_input
        else :
            return "invalid request"
    except Exception as e:
        return e

@app.route('/test/',methods=['GET','POST'])
@login_required
def process():
    return json.dumps(modules.process_query(request.args.get('q'),session['username']))


if __name__ == '__main__':
    app.run(debug = True)
