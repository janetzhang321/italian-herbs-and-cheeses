import sqlite3

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
    query2 = "UPDATE friends SET friend = \'%s\' WHERE user = \'%s\'"%(friendsList, user)
    c.execute(query2)
    db.commit()
    db.close()
    return 1

def deleteFriend(user,oldFriend):
    db=sqlite3.connect(db1)
    c=db.cursor()
    if oldFriend in getFriendList(user):
        friends1 = getFriendList(user)
        friends2 = getFriendList(oldFriend)
        friends1.remove(oldFriend)
        friends2.remove(user)
        newFriendList1_str = ",".join(friends1)
        newFriendList2_str = ",".join(friends2)
        print newFriendList1_str
        print newFriendList2_str
        query1 = "UPDATE friends SET friend = \'%s\' WHERE user = \'%s\'"%(newFriendList1_str, user)
        query2 = "UPDATE friends SET friend = \'%s\' WHERE user = \'%s\'"%(newFriendList2_str, oldFriend)
        c.execute(query1)
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
    print "accept fr"
    query = "DELETE FROM friendRequests WHERE sender = \'%s\' AND receiver = \'%s\'"%(sender,receiver)
    c.execute(query)
    db.commit()
    db.close()
    addFriend(sender,receiver)
    addFriend(receiver,sender)
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

def htmlify_Friends(user):
    friendList = getFriendList(user)
    friendList_str = ""
    for entry in friendList:
        if entry != "":
            friendList_str+="<div class='friendList_button'>"
            friendList_str+='''%s <button class="btn btn-danger btn-xs yeboi"><span class="glyphicon glyphicon-remove"></span></button>'''%(entry) #href= ajax to call js function accept fr
            friendList_str+="</div><br>"
    return friendList_str

def htmlify_FriendRequests(user):
    friendRequestList = getFriendRequests(user)
    friendRequest_str = ""
    for entry in friendRequestList:
        friendRequest_str+="<div class='friendRequest_button'>"
        friendRequest_str+='''%s <button class="btn btn-success btn-xs noboi"><span class=" glyphicon glyphicon-ok"></span></button>'''%(entry) #href= ajax to call js function accept fr
        friendRequest_str+=''' <button class="btn btn-danger btn-xs wtfboi"><span class="glyphicon glyphicon-remove"></span></button>'''
        friendRequest_str+="</div><br>"
    return friendRequest_str
    
    
