import hashlib,sqlite3

f="database.db"

db = sqlite3.connect(f) #open if f exists, otherwise create
c = db.cursor()    #facilitate db ops

q = "CREATE TABLE users (user TEXT, password TEXT)"
c.execute(q)
#q = "INSERT INTO users VALUES(\'%s\',\'%s\')" %("admin","test")
#c.execute(q)

q = "CREATE TABLE profiles (user TEXT, about TEXT)"
c.execute(q)
#q = "INSERT INTO profiles VALUES(\'%s\',\'%s\')" %("admin","test")
#c.execute(q)

q = "CREATE TABLE friends (user TEXT, friend TEXT)"
c.execute(q)
#q = "INSERT INTO friends VALUES(\'%s\',\'%s\',\'%s\')" %("admin","test","request")
#c.execute(q)

q = "CREATE TABLE friendRequests (sender TEXT, receiver TEXT)"
c.execute(q)
#q = "INSERT INTO friendRequests VALUES(\'%s\',\'%s\')" %("admin","test")
#c.execute(q)

q = "CREATE TABLE chatRooms (roomId TEXT, username TEXT)"
c.execute(q)

q = "CREATE TABLE chatNames (roomId TEXT, roomName TEXT)"
c.execute(q)

q = "CREATE TABLE chatMessages (roomId TEXT, username TEXT, msg TEXT, hora TEXT)"
c.execute(q)

db.commit() #save changes
db.close()  #close database
