import hashlib,sqlite3

f="database.db"

db = sqlite3.connect(f) #open if f exists, otherwise create
c = db.cursor()    #facilitate db ops

q = "CREATE TABLE users (username TEXT, password TEXT)"
c.execute(q)
q = "INSERT INTO users (\'%s\',\'%s\')" %("admin","test")
c.execute(q)

q = "CREATE TABLE profiles (username TEXT, about TEXT)"
c.execute(q)
q = "INSERT INTO profiles (\'%s\',\'%s\')" %("admin","test")
c.execute(q)

q = "CREATE TABLE friends (username TEXT, friend TEXT)"
c.execute(q)
q = "INSERT INTO friends (\'%s\',\'%s\')" %("admin","test")
c.execute(q)

q = "CREATE TABLE blocked (username TEXT, friend TEXT)"
c.execute(q)
q = "INSERT INTO blocked (\'%s\',\'%s\')" %("admin","test")
c.execute(q)

db.commit() #save changes
db.close()  #close database
