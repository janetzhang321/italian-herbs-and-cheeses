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
    query2 = "INSERT INTO friends VALUES(\'%s\',\"\")" %(user)
    c2.execute(query2)
    
    #c3=db.cursor()
    #query3 = "INSERT INTO friendRequests VALUES(\'%s\',\"\")" %(user)
    #c3.execute(query3)
    
    c4=db.cursor()
    query4 = "INSERT INTO blocks VALUES(\'%s\',\"\")" %(user)
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
    preFriendsList = ""
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
    return 1

def addFriendRequest(sender,receiver):
    db=sqlite3.connect(db1)
    c=db.cursor()
    query1 = "SELECT * FROM friendRequests"
    friendRequestsList = c.execute(query1)
    for entry in friendRequestsList:
        if (entry[0]==sender and entry[1]==receiver): return 0
    query2 = "INSERT INTO friendRequests VALUES(\'%s\',\'%s\')"%(sender,receiver)
    c.execute(query2)
    db.commit()
    db.close()
    return 1

def acceptFriendRequest(sender,receiver):
    db=sqlite3.connect(db1)
    c=db.cursor()
    query = "DELETE FROM friendRequests WHERE sender = \'%s\' AND receiver = \'%s\'"%(sender,receiver)
    c.execute(query)
    addFriend(user,receiver)
    addFriend(receiver,user)
    db.commit()
    db.close()
    return 1

#not tested
def addBlock(user,blocked):
    db=sqlite3.connect(db1)
    c=db.cursor()
    query1 = "SELECT blocked FROM blocks WHERE user = \'%s\'"(user)
    blocks = c.execute(query1)
    for entry in blocks:
        if (entry==blocked): return 0
    query2 = "INSERT INTO blocks VALUEs(\'%s\',\'%s\')"%(user,blocked)
    c.execute(query2)
    db.commit()
    db.close()
    return 1

#not tested
def removeBlock(user,blocked):
    db=sqlite3.connect(db1)
    c=db.cursor()
    query = "DELETE FROM blocks WHERE user = \'%s\' AND blocked = \'%s\'"(user,blocked)
    c.execute(query)
    db.commit()
    db.close()
    return 1

def getFriendList(user):
    db=sqlite3.connect(db1)
    c=db.cursor()
    retList = []
    friendsList=""
    query = "SELECT friend FROM friends WHERE user = \'%s\'"%(user)
    friends = c.execute(query)
    for entry in friends:
        friendsList = entry[0]
    friendsArr = friendsList.split(",")
    for entry in friendsArr:
        retList.append(entry)
    db.close()
    return retList

def getBlocks(user):
    db=sqlite3.connect(db1)
    c=db.cursor()
    retList=[]
    query = "SELECT blocked FROM blocks WHERE user = \'%s\'"%(user)
    blocksList = c.execute(query)
    for entry in blocksList:
        retList.append(entry[0])
    db.commit()
    db.close()
    return retList

def getFriendRequests(user):
    db=sqlite3.connect(db1)
    c=db.cursor()
    retList=[]
    query = "SELECT sender FROM friendRequests WHERE receiver=\'%s\'"%(user)
    friendRequestsList = c.execute(query)
    for entry in friendRequestsList:
        retList.append(entry[0])
    db.commit()
    db.close()
    return retList

def htmlify_FriendRequests(user):
    friendRequestList = getFriendRequests(user)
    friendRequest_str = ""
    for entry in friendRequestList:
        friendRequest_str+="<div class='friendRequest_button'>"
        friendRequest_str+="<a href='/myprofile/'>%s</a>"%(entry) #href= ajax to call js function accept fr
        friendRequest_str+="</div><br>"
    return friendRequest_str
    
    
