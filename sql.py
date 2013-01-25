#!/usr/bin/python
"""TorAuth Module
v1.2 Touya Akira"""

import MySQLdb;

CCHANNEL = '#CONTROL_CHANNEL'
TDB = 'DB NAME'
TTABLE = 'DB TABLE NAME'
THOST = 'DB HOST NAME'
TUSER = 'DB USER NAME'
TPASS = 'DB PASWORD'
badchars = ['\\', '(', ')', '\'', '"', '@']

def thelp(phenny, input):
	if input.sender != CCHANNEL: return
	phenny.say("Usage:")
	phenny.say(".add <ident> <hash> - add a user to tor auth.")
	phenny.say(".del <ident|hash> or .del <ident> <hash> - delete user with matching ident and/or hash from tor auth.")
	phenny.say(".find <ident|hash> - find and display users matching ident or hash.")
	phenny.say(".cident <hash> <newident> - change ident to <newident> for user with <hash>.")
	phenny.say(".chash <ident> <newhash> - change hash to <newhash> for user with <ident>.")
thelp.commands = ['help']

def searchi(phenny, input):
	if (input.sender != CCHANNEL): return
	if not input.group(2):
		phenny.say("No argument give. Syntax: .find <ident|hasj>.")
		return
	if " " in input.group(2):
		phenny.say("More than one argument given. Syntax: .find <ident|hash>")
	for char in badchars:
		if char in input.group(2):
			phenny.say("Invalid characters in arguments detected. Trying to exploit me, "+input.nick+"?")
			return
	else:
		if input.group(2) == "*":
			phenny.say("\002\00303TOR AUTH MESSAGE\003: \002Err, nope. Not gonna flood the channel. Please use the website to list all users, kthx.")
		else:
			if len(input.group(2)) == 64:
				db = MySQLdb.connect(host=THOST, user=TUSER, passwd=TPASS, db=TDB)
				cursor = db.cursor()
				sql = 'SELECT * FROM ' +TTABLE+' WHERE hash = "'+input.group(2)+'"'
				cursor.execute(sql)
				results = cursor.fetchall()
				i = 0
				for row in results:
					i += 1
					rident = row[0]
					rhash = row[1]
					phenny.say("\002\00303TOR AUTH MESSAGE\003: \002"+rident+" "+rhash)
				if i == 1:
					phenny.say("\002\00303TOR AUTH MESSAGE\003: \002"+str(i)+" match found.")
				elif i > 1:
					phenny.say("\002\00303TOR AUTH MESSAGE\003: \002"+str(i)+" matches found.")
				else:
					phenny.say("\002\00303TOR AUTH MESSAGE\003: \002no matches found.")
				db.close()
				return
			db = MySQLdb.connect(host=THOST, user=TUSER, passwd=TPASS, db=TDB)
			cursor = db.cursor()
			sql = 'SELECT * FROM ' +TTABLE+' WHERE ident = "'+input.group(2)+'"'
			#phenny.say("\002\00303TOR AUTH MESSAGE\003: \002sending: "+sql)
			cursor.execute(sql)
			results = cursor.fetchall()
			i = 0;
			for row in results:
				i += 1
				rident = row[0]
				rhash = row[1]
				phenny.say("\002\00303TOR AUTH MESSAGE\003: \002"+rident+" "+rhash)
			if i == 1:
				phenny.say("\002\00303TOR AUTH MESSAGE\003: \002"+str(i)+" match found.")
			elif i > 1:
				phenny.say("\002\00303TOR AUTH MESSAGE\003: \002"+str(i)+" matches found.")
			else:
				phenny.say("\002\00303TOR AUTH MESSAGE\003: \002no matches found.")
			db.close()
searchi.commands = ['find']

def addi(phenny, input):
	if (input.sender != CCHANNEL): return
	if not input.group(2):
		phenny.say("No arguments given. Syntax: .add <ident> <hash>")
		return
	for char in badchars:
		if char in input.group(2):
			phenny.say("Invalid characters in arguments detected. Trying to exploit me, "+input.nick+"?")
			return
	else:
		query = input.group(2).split()
		if len(query) != 2:
			phenny.say("Number of arguments mismatch. Syntax: .add <ident> <hash>")
			return
		if len(query[1]) != 64:
			phenny.say("\002\00303TOR AUTH MESSAGE\003: \002Hash length does not match. Are you sure you have entered a sha256 hash?")
			return
		else:
			db = MySQLdb.connect(host=THOST, user=TUSER, passwd=TPASS, db=TDB)
			cursor = db.cursor()
			sql = 'SELECT * FROM ' +TTABLE+' WHERE ident = "'+query[0]+'"'
			#phenny.say("\002\00303TOR AUTH MESSAGE\003: \002sending: "+sql)
			cursor.execute(sql)
			results = cursor.fetchall()
			i = 0;
			for row in results:
				i += 1
				rident = row[0]
				rhash = row[1]
				phenny.say("\002\00303TOR AUTH MESSAGE\003: \002"+rident+" "+rhash)
			if results:
				phenny.say("rident: "+str(rident))
				if rident == query[0] and rhash == query[1]:
					phenny.say("\002\00304TOR AUTH CRITICAL\003: \002Entry already exists!")
					return
				if rident == query[0]:
					phenny.say("\002\00308TOR AUTH WARNING\003: \002Ident already exists. Adding same ident with a different hash.")
			sql = 'SELECT * FROM ' +TTABLE+' WHERE hash = "'+query[1]+'"'
			cursor.execute(sql)
			results = cursor.fetchall()
			i = 0
			for row in results:
				rident = row[0]
				rhash = row[1]
			if results:
				if rhash == query[1]:
					phenny.say("\002\00308TOR AUTH WARNING\003: \002Hash already exists. Adding same hash to a different ident.")
			ident = (query[0][:10]) if len(query[0]) > 10 else query[0]
			if len(query[0]) > 10: phenny.say("\002\00308TOR AUTH WARNING\003: \002Ident too long (more than 10 characters). Truncating to "+ident+".")
			db = MySQLdb.connect(host=THOST, user=TUSER, passwd=TPASS, db=TDB)
			cursor = db.cursor()
			sql = 'INSERT INTO '+TTABLE+' (ident, hash) VALUES ("'+ident+'", "'+query[1]+'")'
			#phenny.say("\002\00303TOR AUTH MESSAGE\003: \002sending: "+sql)
			cursor.execute(sql)
			db.close()
			phenny.say('\002\00303TOR AUTH MESSAGE\003: \002User with ident "'+ident+'" and hash "'+query[1]+'" added.')
addi.commands = ['add']

def deli(phenny, input):
	if (input.sender != CCHANNEL): return
	if not input.group(2):
		phenny.say("No arguments given. Syntax: .del [ident|hash] or del <ident> <hash>")
		return
	for char in badchars:
		if char in input.group(2):
			phenny.say("Invalid characters in arguments detected. Trying to exploit me, "+input.nick+"?")
			return
	args = []
	if " " in input.group(2): args = input.group(2).split()
	if len(args) > 2:
		phenny.say("More than one argument given. Syntax: .del [ident|hash] or del <ident> <hash>")
		return
	if len(args) > 1:
		if len(args[1]) != 64:
			phenny.say("\002\00303TOR AUTH MESSAGE\003: \002Hash length does not match. Are you sure you have entered a sha256 hash?")
			return
		db = MySQLdb.connect(host=THOST, user=TUSER, passwd=TPASS, db=TDB)
		cursor = db.cursor()
		sql = 'SELECT * FROM ' +TTABLE+' WHERE ident = "'+args[0]+'" AND hash = "'+args[1]+'"'
		cursor.execute(sql)
		results = cursor.fetchall()
		i = 0
		for row in results:
			i += 1;
			rident = row[0]
			rhash = row[1]
		if i == 0:
			phenny.say("No matching entry found.")
			db.close()
			return
		if i == 1:
			sql = 'DELETE FROM '+TTABLE+' WHERE ident = "'+args[0]+'" AND hash = "'+args[1]+'"'
			cursor.execute(sql)
			phenny.say('\002\00303TOR AUTH MESSAGE\003: \002User with ident "'+rident+'" and hash "'+rhash+'" removed from database.')
		db.close()
	else:
		if len(input.group(2)) == 64:
			db = MySQLdb.connect(host=THOST, user=TUSER, passwd=TPASS, db=TDB)
			sql = 'SELECT * FROM ' +TTABLE+' WHERE hash = "'+input.group(2)+'"'
			cursor = db.cursor()
			cursor.execute(sql)
			results = cursor.fetchall()
			i = 0
			for row in results:
				i += 1;
				rident[i] = row[0]
				rhash[i] = row[1]
			if i > 1:
				phenny.say("\002\00304TOR AUTH CRITICAL\003: \002Hash exists more than once. Some users share the same password.")
				phenny.say("\002\00304TOR AUTH CRITICAL\003: \002Please use the syntax .del <ident> <hash> to delete the specific user:")
				db.close()
				return
			db = MySQLdb.connect(host=THOST, user=TUSER, passwd=TPASS, db=TDB)
			cursor = db.cursor()
			sql = 'DELETE FROM '+TTABLE+' WHERE hash = "'+input.group(2)+'"'
			#phenny.say("\002\00303TOR AUTH MESSAGE\003: \002sending: "+sql)
			cursor.execute(sql)
			db.close()
			phenny.say("\002\00303TOR AUTH MESSAGE\003: \002User with hash "+input.group(2)+" deleted.")
		else:
			db = MySQLdb.connect(host=THOST, user=TUSER, passwd=TPASS, db=TDB)
			cursor = db.cursor()
			sql = 'SELECT * FROM '+TTABLE+' WHERE ident = "'+input.group(2)+'"'
			cursor.execute(sql)
			results = cursor.fetchall()
			i = 0
			for row in results:
				i += 1
				rident = row[0]
				#rhash = row[1]
			if i == 0:
				phenny.say("\002\00303TOR AUTH MESSAGE\003: \002no matching idents or hashes found.")
				return
			elif i > 1:
				phenny.say("\002\00303TOR AUTH MESSAGE\003: \002more than one matching idents or hashes found. Please use .del <ident> <hash> to remove user.")
				return
			else:
				sql = 'DELETE FROM '+TTABLE+' WHERE ident = "'+input.group(2)+'"'
				cursor.execute(sql)
				phenny.say('\002\00303TOR AUTH MESSAGE\003: \002User with ident "'+rident+'" removed from database.')
			db.close()
deli.commands = ['del']

def cident(phenny, input):
	if (input.sender != CCHANNEL): return
	if not input.group(2):
		phenny.say("No arguments given. Syntax: .cident <hash> <ident>")
		return
	for char in badchars:
		if char in input.group(2):
			phenny.say("Invalid characters in arguments detected. Trying to exploit me, "+input.nick+"?")
			return
	else:
		query = input.group(2).split()
		db = MySQLdb.connect(host=THOST, user=TUSER, passwd=TPASS, db=TDB)
		cursor = db.cursor()
		sql = 'SELECT * FROM '+TTABLE+' WHERE hash = "'+query[0]+'"'
		#phenny.say(sql)
		cursor.execute(sql)
		results = cursor.fetchall()
		i = 0;
		for row in results:
			i += 1
			rident = row[0]
			rhash = row[1]
			#phenny.say("\002\00303TOR AUTH MESSAGE\003: \002"+rident+" "+rhash)
		if i == 0: 
			phenny.say('Hash not found.')
			return
		elif i > 1:
			phenny.say('\002\00304TOR AUTH CRITICAL\003: \002More than one hash found. Aborting. (This means two or more users are sharing passwords')
		else:
			sql = 'UPDATE '+TTABLE+' SET ident = "'+query[1]+'" WHERE hash = ("'+query[0]+'")'
			#phenny.say("\002\00303TOR AUTH MESSAGE\003: \002sending: "+sql)
			cursor.execute(sql)
			phenny.say('\002\00303TOR AUTH MESSAGE\003: \002Ident for hash "'+rhash+'" changed from "'+rident+'" to "'+query[1]+'".')
		db.close()
cident.commands = ['cident']

def chash(phenny, input):
	if (input.sender != CCHANNEL): return
	if not input.group(2):
		phenny.say("No arguments given. Syntax: .chash <ident> <hash>")
		return
	for char in badchars:
		if char in input.group(2):
			phenny.say("Invalid characters in arguments detected. Trying to exploit me, "+input.nick+"?")
			return
	else:
		query = input.group(2).split()
		db = MySQLdb.connect(host=THOST, user=TUSER, passwd=TPASS, db=TDB)
		cursor = db.cursor()
		sql = 'SELECT * FROM '+TTABLE+' WHERE ident = "'+query[0]+'"'
		#phenny.say('DEBUG '+sql)
		cursor.execute(sql)
		results = cursor.fetchall()
		i = 0;
		for row in results:
			i += 1
			rident = row[0]
			rhash = row[1]
			#phenny.say("DEBUG "+rident+" "+rhash)
		if i == 0: 
			phenny.say('ident not found.')
			return
		elif i > 1:
			phenny.say('\002\00304TOR AUTH CRITICAL\003: \002More than one matching ident found. Aborting. Please .del the entry and .add with new ident, kthx.')
		else:
			sql = 'UPDATE '+TTABLE+' SET hash = "'+query[1]+'" WHERE ident = ("'+query[0]+'")'
			#phenny.say("DEBUG "+sql)
			cursor.execute(sql)
			phenny.say('\002\00303TOR AUTH MESSAGE\003: \002Hash for ident "'+rident+'" changed from "'+rhash+'" to "'+query[1]+'".')
		db.close()
chash.commands = ['chash']
