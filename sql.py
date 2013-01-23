#!/usr/bin/python
"""TorAuth Module
v1.1 Touya Akira"""

import MySQLdb;

CCHANNEL = "OPER CHANNEL"
TTABLE = 'DB TABLE'
THOST = 'DB HOST'
TUSER = 'DB USER'
TPASS = 'DB PASS'
TDB = 'DB NAME'

def thelp(phenny, input):
	phenny.say("Usage:")
	phenny.say(".add <ident> <hash> - add a user to tor auth.")
	phenny.say(".del <hash> - delete user with matching hash from tor auth.")
	phenny.say(".find <ident> - find and display users matching ident.")
thelp.commands = ['help']

def searchi(phenny, input):
	if (input.sender != CCHANNEL): return
	else:
		if input.group(2) == "*":
			phenny.say("\002TOR AUTH: \002Err, nope. Not gonna flood the channel. Please use the website to list all users, kthx.")
		else:	
			db = MySQLdb.connect(host=THOST, user=TUSER, passwd=TPASS, db=TDB)
			cursor = db.cursor()
			sql = 'SELECT * FROM ' +TTABLE+' WHERE ident = "'+input.group(2)+'"'
			phenny.say("\002TOR AUTH: \002sending: "+sql)
			cursor.execute(sql)
			results = cursor.fetchall()
			i = 0;
			for row in results:
				i += 1
				rident = row[0]
				rhash = row[1]
				phenny.say("\002TOR AUTH: \002"+rident+" "+rhash)
			phenny.say("\002TOR AUTH: \002All matches displayed.")
			db.close()
searchi.commands = ['find']		

def addi(phenny, input):
	if (input.sender != CCHANNEL): return
	else:
		query = input.group(2).split()
		if len(query[1]) != 64:
			phenny.say("\002TOR AUTH: \002Hash length does not match. Are you sure you have entered a sha256 hash?")
			return
		else:
			db = MySQLdb.connect(host=THOST, user=TUSER, passwd=TPASS, db=TDB)
			cursor = db.cursor()
			sql = 'INSERT INTO '+TTABLE+' (ident, hash) VALUES ("'+query[0]+'", "'+query[1]+'")'
			phenny.say("\002TOR AUTH: \002sending: "+sql)
			cursor.execute(sql)
			db.close()
			phenny.say("\002TOR AUTH: \002User "+query[0]+" added.")
addi.commands = ['add']

def deli(phenny, input):
	if (input.sender != CCHANNEL): return
	else:
		if len(input.group(2)) != 64:
			phenny.say("Hash length does not match. Are you sure you have entered a sha256 hash?")
			return
		else:
			db = MySQLdb.connect(host=THOST, user=TUSER, passwd=TPASS, db=TDB)
			cursor = db.cursor()
			sql = 'DELETE FROM '+TTABLE+' WHERE hash = "'+input.group(2)+'"'
			phenny.say("\002TOR AUTH: \002sending: "+sql)
			cursor.execute(sql)
			db.close()
			phenny.say("\002TOR AUTH: \002User with hash "+input.group(2)+" deleted.")
deli.commands = ['del']

