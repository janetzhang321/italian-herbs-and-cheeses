
from flask import Flask, render_template, request, url_for, session, redirect
from flask_socketio import SocketIO, emit
from datetime import datetime
from utils import login, users, chat


db = "data/database.db"

app = Flask(__name__)
app.config['SECRET_KEY'] = 'shhhh'

socketio = SocketIO(app)


@socketio.on('joined')
def handle_connections(msg):
    socketio.emit('status',{'msg': session['Username'] + ' has entered the room.' });

@socketio.on('message')
def handle_messages(msgy):
    socketio.emit('send',  {'msg': session['Username'] + ': ' + msgy['msg'] });




@app.route("/")
def root():
    if 'Username' not in session:
        return redirect(url_for("log"))
    else:
        return redirect(url_for("home"))

@app.route("/home/", methods = ['GET','POST'])
def home():
    if 'Username' not in session:
        return redirect(url_for("log"))
    else:
        chatrooms = chat.getChatrooms()
        return render_template("home.html",user=session['Username'],chatrooms=chatrooms)

@app.route("/login/")
def log():
    status = request.args.get("status")
    return render_template("login.html",status=status)

@app.route("/authenticate/", methods=['POST'])
def authenticate():

    user = request.form["user"]
    password = request.form["pass"]
    action = request.form["action"]#login vs. register

    if action == "Register":
        regRet = login.register(user,password)#returns an error/success message
        if regRet == 1:
            session["Username"] = user
            users.initUserDB(user)
            return redirect(url_for('home'))#,success="You have registered"))
        else:
            return redirect(url_for('log', status=regRet))

    if action == "Login":
        text = login.login(user,password)#error message
        print text
        if text == "":#if no error message, succesful go back home
            session["Username"] = user
            return redirect(url_for('home'))#,success="You have logged in"))
        return redirect(url_for('log', status=text))

@app.route("/addfriend/", methods=["POST"])
def addFriend():
    newFriend = request.form["newFriend"]
    users.addFriend(session["Username"],newFriend)
    return redirect(url_for("home"))

#@app.route("/myprofile/")
#def myProfile():
#    return render_template(

@app.route("/vid/")
def video():
    return render_template("minivid.html")

@app.route("/logout/")
def logout():
    if "Username" in session: 
        session.pop("Username")
    return redirect(url_for("log"))




@app.route("/chat/<identifier>", methods=['GET','POST'])
def room(identifier):
    user = session['Username']
    room = identifier
    return render_template("chatroom.html",user=user,room=room)


if __name__ == "__main__":
    app.debug = True
    socketio.run(app)



