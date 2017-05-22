from flask import Flask, render_template, request, url_for, session, redirect
import hashlib, sqlite3
import datetime
import json
import thread
import time
import uuid
from Queue import Queue
from datetime import datetime
from utils import login, users

db = "data/database.db"

app = Flask(__name__)
app.config['SECRET_KEY'] = 'sec-c-YWE3Zjg2NDgtMGRjMC00NzAzLTliZTQtZDEyNDI3NThmMmY2'
app.debug = True


@app.route("/")
def root():
    if 'Username' not in session:
        return redirect(url_for("log"))
    else:
        return redirect(url_for("home"))


@app.route("/home/", methods = ["GET","POST"])
def home():
    if 'Username' not in session:
        return redirect(url_for("log"))
    else:
        return render_template("home.html")

@app.route("/login/")
def log():
    status = request.args.get("status")
    return render_template("login.html",status=status)

@app.route('/authenticate/', methods=['POST'])
def authenticate():

    pw = request.form["pass"]
    un = request.form["user"]
    tp = request.form["action"]#login vs. register

    if tp == "Register":
        regRet = login.register(un,pw)#returns an error/success message
        if regRet == 1:
            session["Username"] = un
            return redirect(url_for('home'))#,success="You have registered"))
        else:
            return redirect(url_for('home'))#,error=regRet))

    if tp == "Login":
        text = login.login(un,pw)#error message
        if text == "":#if no error message, succesful go back home
            session["Username"] = un
            return redirect(url_for('home'))#,success="You have logged in"))
        return redirect(url_for('home'))#,error=text))



@app.route("/logout/")
def logout():
    if "Username" in session: 
        session.pop("Username")
    return redirect(url_for("log"))

if __name__ == "__main__":
    app.debug = True
    app.run()



