from flask import Flask, render_template, request, url_for, session, redirect
import hashlib, sqlite3

db1 = "data/database.db"

def initUserDB(user):
    db=sqlite3.connect(db1)
    c0=db.cursor()
    query0 = "INSERT INTO users VALUES(\'%s\',\"\")" %(user)
    c0.execute(query0)

    c1=db.cursor()
    query1 = "INSERT INTO profiles VALUES(\'%s\',\"\")" %(user)
    c1.execute(query1)
    
    c2=db.cursor()
    query2 = "INSERT INTO friends VALUES(\'%s\',\"\",\"\")" %(user)
    c2.execute(query2)
    
    c3=db.cursor()
    query3 = "INSERT INTO friendRequests VALUES(\'%s\',\"\")" %(user)
    c3.execute(query3)
    
    c4=db.cursor()
    query4 = "INSERT INTO blocked VALUES(\'%s\',\"\")" %(user)
    c4.execute(query4)

    db.commit()
    db.close()

def editProfile(user,about):
    db=sqlite3.connect(db1)
    c=db.cursor()
    query = "UPDATE profiles SET about = \'%s\' WHERE user = \'%s\'"%(about, user)
    db.commit()
    db.close()
    return "success"

def addFriend(user,newFriend):
    db=sqlite3.connect(db1)
    c=db.cursor()
    query1 = "SELECT friend FROM friends WHERE user = \'%s\'"%(user)
    item = c.execute(query1)
    for entry in item:
        preFriendsList = entry[0]
    if (preFriendsList == ""):
        friendsList = newFriend
    else:   
        friendsList = preFriendsList + ",%s"%(newFriend)
    print friendsList
    query2 = "UPDATE friends SET friend = \'%s\' WHERE user = \'%s\'"%(friendsList, user)
    c.execute(query2)
    db.commit()
    db.close()
    return "success"

def addFriendRequest(user,FriendRequest):
    db=sqlite3.connect(db1)
    c=db.cursor()
    query1 = "SELECT friendRequest FROM friendRequests WHERE users = \'%s\'"%(user)
    item = c.execute(query1)
    for entry in item:
        requests = entry[0]
    requestsArr = requests.split(",")
    if (FriendRequest in requestsArr): return "request already sent"  

    if (requests == ""):
        requests = FriendRequest
    else:
        requests = requests + ",%s"%(FriendRequest)
    query2 = "UPDATE friendRequests SET request = \'%s\' WHERE user = \'%s\'"%(FriendRequest,user)
    db.commit()
    db.close()
    return "success"

def getFriendList(user):
    db=sqlite3.connect(db1)
    c=db.cursor()
    retList = []
    query = "SELECT friend FROM friends WHERE user = \'%s\'"%(user)
    friends = c.execute(query1)
    for entry in friends:
        friendsList = entry[0]
    friendsArr = friendsList.split(",")
    for entry in friendsArr:
        retList.append(entry)
    db.close()
    return retList


    
    
