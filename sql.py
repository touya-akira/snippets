#!/usr/bin/python

import MySQLdb;

CCHANNEL = ""
TTABLE = ''
THOST = ''
TUSER = ''
TPASS = ''
TDB = ''

def thelp(phenny, input):
	phenny.say("Usage:")
	phenny.say(".add <ident> <hash> - add a user to tor auth.")
	phenny.say(".del <hash> - delete user with matching hash from tor auth.")
	phenny.say(".find <ident> - find and display users matching ident.")
thelp.commands = ['help']

def searchi(phenny, input):
	if (input.sender != CCHANNEL): return
	else:
		db = MySQLdb.connect(host=THOST, user=TUSER, passwd=TPASS, db=TDB)
		cursor = db.cursor()
		sql = 'SELECT * FROM ' +TTABLE+' WHERE ident = "'+input.group(2)+'"'
		phenny.say(sql)
		cursor.execute(sql)
		results = cursor.fetchall()
		for row in results:
			rident = row[0]
			rhash = row[1]
			phenny.say(rident+" "+rhash)
		db.close()
searchi.commands = ['find']		

def addi(phenny, input):
	if (input.sender != CCHANNEL): return
	else:
		query = input.group(2).split()
		if len(query[1]) != 64:
			phenny.say("Hash length does not match. Are you sure you have entered a sha256 hash?")
			return
		else:
			db = MySQLdb.connect(host=THOST, user=TUSER, passwd=TPASS, db=TDB)
			cursor = db.cursor()
			sql = 'INSERT INTO '+TTABLE+' (ident, hash) VALUES ("'+query[0]+'", "'+query[1]+'")'
			phenny.say(sql)
			cursor.execute(sql)
			db.close()
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
			phenny.say(sql)
			cursor.execute(sql)
			db.close()
deli.commands = ['del']

