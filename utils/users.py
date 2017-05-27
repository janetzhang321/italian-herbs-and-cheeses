from flask import Flask, render_template, request, url_for, session, redirect
import hashlib, sqlite3

db1 = "data/database.db"

def editProfile(username,about):
    db=sqlite3.connect(db1)
    c=db.cursor()
    query = "UPDATE profiles SET about = \'%s\' WHERE username = \'%s\'"%(about, username)
    db.commit()
    db.close()
    return "success"

def addFriend(username,newFriend):
    db=sqlite3.connect(db1)
    c=db.cursor()
    d=db.cursor()
    query1 = "SELECT friend FROM friends WHERE username = \'%s\'"%(username)
    preFriendsList = c.execute(query1)
    friendsList = preFriendsList + ",%s"%(newFriend)
    query2 = "UPDATE friends SET friend = \'%s\' WHERE username = \'%s\'"%(friendsList, username)
    db.commit()
    db.close()
    return "success"

def addFriendRequest(username,FriendRequest):
    db=sqlite3.connect(db1)
    c=db.cursor()
    query = "UPDATE friends SET request = \'%s\' WHERE username = \'%s\'"%(FriendRequest,username)
    db.commit()
    db.close()
    return "success"

    
    
