from flask import Flask, render_template, request, url_for, session, redirect
import hashlib, sqlite3
import datetime
import json
import thread
import time
import uuid
from Queue import Queue
from datetime import datetime

db = "data/database.db"

app = Flask(__name__)
app.config['SECRET_KEY'] = 'sec-c-YWE3Zjg2NDgtMGRjMC00NzAzLTliZTQtZDEyNDI3NThmMmY2'
app.debug = True

@app.route("/")
@app.route("/home/", methods = ["GET","POST"])
def home():
    if 'user' not in session:
        return redirect(url_for("login"))
    else:
        return render_template("home.html")

@app.route("/login/", methods = ["GET","POST"])
def login():
    if "user" in session:
        return redirect(url_for("home"))
    if request.method == "GET":
        return render_template("login.html", status = "")
    if request.form["enter"] == "Register":
        register_message = auth.register(request.form["user"],request.form["pass"])
        return render_template("login.html", status = register_message)
    if request.form["enter"] == "Login":
        login_message = auth.checkLogin(request.form["user"],request.form["pass"])
        if (login_message == ""):
            session["user"] = request.form["user"]
            return redirect(url_for("home"))
    return render_template("login.html", status = login_message)

@app.route("/vid/")
def video():
    return render_template("minivid.html")

    
#@app.route("/profile/", methods = ["POST", "GET"])
#def profile():
#    if "user" not in session:
#        return redirect(url_for("login"))
#    if request.method =="GET":
#        return render_template("accountSettings.html")
#    else: pass_message = auth.changePass(session["user"],request.form["oldpass"],request.form["newpass"])
#    return render_template("accountSettings.html", status = pass_message)

@app.route("/logout/")
def logout():
    if "user" in session: session.pop("user")
    return redirect(url_for("home"))

if __name__ == "__main__":
    app.debug = True
    app.run()



