import hashlib
import sqlite3

def createRoom(username):

	number = 5
	id = sha1(number.encode('utf-8')).hexdigest()
	return id

def getChatrooms():
	return []
def roomName(id):
	return ""

