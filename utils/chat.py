import sqlite3
import string
import random
import os

db1 = "data/database.db"

#generate random string id
def generateId(size=10, chars=string.ascii_uppercase + string.ascii_lowercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


def createRoom(roomName,username,username2):
    db=sqlite3.connect(db1)
    c=db.cursor()
    

    roomId = generateId()

    query1 = "INSERT INTO chatNames VALUES (?,?)"
    c.execute(query1,(roomId,roomName))

    query2 = "INSERT INTO chatRooms VALUES (?,?)"
    query3 = "INSERT INTO chatRooms VALUES (?,?)"
    c.execute(query2,(roomId,username))
    c.execute(query3,(roomId,username2))

        
    db.commit()
    db.close()
    return roomId

def addUserToRoom(username,roomId):
    db=sqlite3.connect(db1)
    c=db.cursor()

    query1 = "SELECT * FROM chatRooms WHERE roomId=? and username=?"
    records = c.execute(query1,(roomId,username))


    for record in records:
        break
    else:
        query2 = "INSERT INTO chatRooms VALUES (?,?)"
        c.execute(query2,(roomId,username))

        db.commit()
        db.close()
        return True #user added
    db.close()
    return False #user not added because user is already in chatroom

def getChatRooms(username):
    ans = []

    db=sqlite3.connect(db1)
    c=db.cursor()

    query1 = "SELECT roomId FROM chatRooms WHERE username=?"
    records = c.execute(query1,(username,))
    for x in records:
        ans.append(x[0])
    db.close()
    return ans

def getRoomName(id):
    db=sqlite3.connect(db1)
    c=db.cursor()

    query1 = "SELECT roomName FROM chatNames WHERE roomId=?"
    records = c.execute(query1,(roomId,))
    
    for record in records:
        return record[0]
    else:
        return "UNNAMED"
    db.close()

def deleteRoom(roomId):
    db = sqlite3.connect(db1)
    c = db.cursor()

    data = c.execute("DELETE FROM chatRooms WHERE roomId=?", (roomId,))
    data = c.execute("DELETE FROM chatNames WHERE roomId=?", (roomId,))

    db.commit()
    db.close()

def leaveRoom(username,roomId):
    db = sqlite3.connect(db1)
    c = db.cursor()

    data = c.execute("DELETE FROM chatRooms WHERE username=? and roomId=?", (username,roomId))
    
    db.commit()
    db.close()

def getUsersIn(roomId):
    ans = []
    
    db = sqlite3.connect(db1)
    c = db.cursor()
    data = c.execute("SELECT username FROM chatRooms WHERE roomId=?",(roomId,))

    for x in data:
        ans.append(x[0])

    db.close()
    return ans

#tests
if __name__ == '__main__':
    os.chdir("..")
    roomId = createRoom("hello","michael","harry")
    print roomId
    print getUsersIn(roomId)
    leaveRoom("harry",roomId)
    print getUsersIn(roomId)
    addUserToRoom("lindsey",roomId)
    print getUsersIn(roomId)
    print getRoomName(roomId)
    print getChatRooms("michael")
    for roomId in getChatRooms("michael"):
        deleteRoom(roomId)
    print getChatRooms("lindsey")
    print getChatRooms("michael")
    