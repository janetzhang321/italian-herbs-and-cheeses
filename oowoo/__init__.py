from flask import Flask, render_template, request, url_for, session, redirect, jsonify
from flask_socketio import join_room, leave_room, SocketIO, emit
from time import localtime, strftime
from utils import login, users, chat
import json
import os

DIR = os.path.dirname(__file__)
DIR += '/'
db = DIR + "data/database.db"

app = Flask(__name__)
app.config['SECRET_KEY'] = 'shhhh'

socketio = SocketIO(app)


@socketio.on('joined')
def handle_connections(data):
    username = session['Username']
    room = data['room']
    join_room(room)
    time = strftime("%H:%M", localtime())
    socketio.emit('status', {'msg': username + ' has entered the room.', 'time':time,'username':username }, room=room);

@socketio.on('message')
def handle_messages(data):
    username = session['Username']
    room = data['room']
    msg = data['msg']
    time = strftime("%m-%d %H:%M", localtime())
    chat.addMessage(room,username,msg,time)
    socketio.emit('send',  {'msg': msg, 'time':time,'username':username },room=room);

@socketio.on('leave')
def handle_leaving(data):
    username = session['Username']
    room = data['room']
    leave_room(room)
    time = strftime("%H:%M", localtime())
    socketio.emit('status', {'msg': username + ' has left the room.', 'time':time}, room=room)
    

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
        username=session['Username']
        friends = users.getFriendList(username)
        chatRooms = chat.getChatRooms(username)
        options = chat.htmlify_dropdownFriends(username)

        return render_template("home.html",user=username,chatRooms=chatRooms,friends=friends,options=options)

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
        if text == "":#if no error message, succesful go back home
            session["Username"] = user
            return redirect(url_for('home'))#,success="You have logged in"))
        return redirect(url_for('log', status=text))

@app.route("/addfriend/", methods=["POST"])
def addFriend():
    newFriend = request.form["newFriend"]
    user = session["Username"]
    error_msg = ""
    if not (users.addFriendRequest(user,newFriend)): error_msg = "That username does not exist"
    return redirect(url_for("home", status = error_msg))

@app.route("/acceptFriendRequest/",methods=["POST"])
def acceptFriendRequest():
    user = request.form['user'].strip()
    friend = request.form['friend'].strip()
    users.acceptFriendRequest(friend,user)
    return jsonify(myFriendRequests=users.htmlify_FriendRequests(user),myFriends=users.htmlify_Friends(user))

@app.route("/declineFriendRequest/",methods=["POST"])
def declineFriendRequest():
    user = request.form['user'].strip()
    friend = request.form['friend'].strip()
    users.acceptFriendRequest(friend,user)
    users.deleteFriend(user,friend)
    return jsonify(myFriendRequests=users.htmlify_FriendRequests(user))

@app.route("/deleteFriend/",methods=['POST'])
def deleteFriend():
    user = request.form['user'].strip()
    friend = request.form['friend'].strip()
    users.deleteFriend(user,friend)
    return jsonify(myFriends=users.htmlify_Friends(user))

@app.route("/myprofile/")
def myProfile():
    if 'Username' not in session:
        return redirect(url_for("log"))
    user = session["Username"]
    myFriends = users.htmlify_Friends(user)
    myFriendRequests = users.htmlify_FriendRequests(user)
    return render_template("myprofile.html",user=user,myFriends=myFriends,friendRequests=myFriendRequests)

@app.route("/vid/")
def video():
    if 'Username' not in session:
        return redirect(url_for("log"))
    user = session["Username"]
    options = chat.htmlify_dropdownFriends(user)
    return render_template("minivid2.html",user=user,options=options)

@app.route("/logout/")
def logout():
    if "Username" in session: 
        session.pop("Username")
    return redirect(url_for("log"))

@app.route("/createroom/", methods=['GET','POST'])
def createroom():
    roomname = request.form['chatname']
    friend = request.form['friend']
    username = session['Username']
    chat.createRoom(roomname,username,friend)
    return  redirect(url_for("home"))

@app.route("/chat/<identifier>", methods=['GET','POST'])
def room(identifier):
    user = session['Username']
    room = identifier
    return render_template("chatroom.html",user=user,room=room)

@app.route("/getinfo/", methods=['POST'])
def getinfo():
    roomId = request.form['roomId'] 
    roomname = chat.getRoomName(roomId)
    users = chat.getUsersIn(roomId)
    messages = chat.getMessagesFor(roomId)
    return jsonify(roomname = roomname,users = users,messages = messages)

@app.route("/deleteRoom/<id>")
def deleteRoom(id):
    chat.deleteRoom(id)
    return redirect(url_for('home'))



if __name__ == "__main__":
    app.debug = False
    socketio.run(app)



