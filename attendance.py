from ldap3 import Server, Connection, AUTO_BIND_NO_TLS, SUBTREE, ALL_ATTRIBUTES
import datetime
import time
import os
import csv
import routes
from bottle import redirect, template
from pymongo import MongoClient
from bson.objectid import ObjectId

client = MongoClient(connect=False)
db = client.attendance
usercol = db.users
classcol = db.classes
## Checks if User Exists in LDAP
def usercheck(searchkey, userinput, inputtype):
	with Connection(Server('192.168.115.5', port=389, use_ssl=False),
			auto_bind=AUTO_BIND_NO_TLS,
			read_only=True,
			check_names=True,
			user='ldap2@nwmc.kwaustinnw.com', password='ldap') as c:
		c.search(search_base='OU=Agents,DC=nwmc,DC=kwaustinnw,DC=com',
			search_filter='(&('+searchkey + userinput + '))',
			attributes=['cn'],
			search_scope=SUBTREE,)
	try:
		output = c.response
		cnuser = output[0]['attributes']
		user = (cnuser['cn'])
		cn = user[0]
		agentname = cn
		agentinput = userinput
		checkintime = checkintime=time.strftime('%m-%d-%Y %H:%M:')
		classname = readclass()
		usercol.find_one_and_update({"agentname":agentname},{"$addToSet":{"classinfo":{"classname": classname,"classdate": checkintime, "agentinput": agentinput}}},upsert=True)
		classcol.find_one_and_update({"activeclass":True},{"$addToSet":{"attended":{"agentname" : agentname, "checkintime": checkintime, "userinput": agentinput}}},upsert=True)
		status = ('Success! Attendance Recorded for: ' +agentname)
		return status 
	except IndexError:
		if inputtype == 'card':
			status= "Error! Card Not Found, Try Social."
			return status
		else:
			status= "Error! Social not found." 
			return status

def manualinput(agentname):
	agentinput = "Manual Input"
	classname = readclass()
	checkintime = time.strftime('%m-%d-%Y %H:%M:')
	usercol.find_one_and_update({"agentname":agentname},{"$addToSet":{"classinfo":{"classname": classname,"classdate": checkintime, "agentinput": agentinput}}},upsert=True)
	classcol.find_one_and_update({"activeclass":True},{"$addToSet":{"attended":{"agentname" : agentname, "checkintime": checkintime, "userinput": agentinput}}},upsert=True)
	status = ('Success! Attendance Recorded for: ' +agentname + '. Support has been notified.')
	return status

#### Class Setting Functions ### 
def readclass():
	query = classcol.find_one({'activeclass': True})
	try: 
		classname = query['classname']
		return classname
	except:
		return False

def setclass(currentclass):
		query = readclass()
		if query is False:
			classtime = time.strftime('%m-%d-%Y')
			setclass = classcol.insert_one({"classname":currentclass+': '+classtime,"date":classtime,"activeclass":True})
			classid = setclass.inserted_id
			query = classcol.find_one({'_id': classid})
			currentclass = query['classname']
			return currentclass
		else:
			return False

def endclass():
	query = readclass()
	if query is False:
		return False
	else:
		classcol.find_one_and_update({'activeclass': True},{"$set": {'activeclass': False}})
		return
	
### Reporting Functions ##

def currentclassreport():
	query = classcol.find_one({'activeclass': True})
	try:
		agentinfo = query['attended']
		agentname = [i['agentname'] for i in agentinfo]
		checkintime = [i['checkintime'] for i in agentinfo]
		inputmethod = [i['userinput'] for i in agentinfo]
		currentreport = list(zip(agentname,checkintime,inputmethod))
		return currentreport
	except:
		currentreport = [('NoInfo', 'NoInfo', 'NoInfo')]
		return currentreport
## Change this function to count any class. ##
def countcurrentclass():
	try:
		query = classcol.find_one({'activeclass': True})
		agentinfo = query['attended']
		agentcount = len(agentinfo)
		return agentcount
	except:
		agentcount = '0'
		return agentcount

def countclass(classname):
	query = classcol.find_one({'classname': classname})
	try:
		agentinfo = query['attended']
		agentcount = len(agentinfo)
		return agentcount
	except:
		agentcount = 0
		return agentcount

def getagentstats(agentname):
	try:
		query = usercol.find_one({'agentname': agentname})
		agentinfo = query['classinfo']
		classname = [i['classname'] for i in agentinfo]
		classdate = [i['classdate'] for i in agentinfo]
		inputmethod = [i['agentinput'] for i in agentinfo]
		agentreport = list(zip(classname,classdate,inputmethod))
		return agentreport
	except:
		return None

def getclasslist():
	query = classcol.find({'activeclass':{'$ne':True}})
	querytolist = list(query)
	try:
		classname = [i['classname'] for i in querytolist]
		classtime = [i['date'] for i in querytolist]
		classlist = list(zip(classname,classtime))
		return classlist
	except:
		return "No Classes!"

def getclass_stats(classname):
	try:
		query = classcol.find_one({'classname': classname})
		classinfo = query['attended']
		agentname = [i['agentname'] for i in classinfo]
		checkintime = [i['checkintime'] for i in classinfo]
		inputmethod = [i['userinput'] for i in classinfo]
		classreport = list(zip(agentname,checkintime,inputmethod))
		return classreport
	except:
		return

###  Class/Agent Management Functions ###
def classtocsv(classname):
	output = getclass_stats(classname)
	csvout = output
	with open('static/temp/%s.csv' %classname, 'w') as f:
		writer = csv.writer(f, delimiter=',', lineterminator='\n')
		writer.writerows(csvout)
		return 

def agent_to_csv(agentname):
	output = getagentstats(agentname)
	csvout = output
	with open('static/temp/%s.csv' %agentname, 'w') as f:
		writer = csv.writer(f, delimiter=',', lineterminator='\n')
		writer.writerows(csvout)
		return 

## Delete agent from Class##
def delagentfromclass(classname,agentname):
		classcol.update({"classname":classname},{"$pull":{"attended":{"agentname":agentname}}})
		usercol.update({"agentname":agentname},{"$pull":{'classinfo':{'classname':classname}}})
		return

## Delete Entire Class##
def deleteclass(classname):
	classcol.delete_one({"classname":classname})
	usercol.delete_many({'classinfo':{'classname':classname}})
	return

## Manually Add Agent to Class ##
def manualAgentAdd(classname,agentname):
	query = classcol.find_one({'classname': classname})
	checkintime = time.strftime('%m-%d-%Y %H:%M:')
	classcol.find_one_and_update({"classname":classname},{"$addToSet":{"attended":{"agentname" : agentname, "checkintime": checkintime, "userinput": "Added by Admin"}}},upsert=True)
	usercol.find_one_and_update({"agentname":agentname},{"$addToSet":{"classinfo":{"classname": classname,"classdate": checkintime, "agentinput": "Added by Admin"}}},upsert=True)
	return
## List All Agents in the User Collection(usercol) ##
def listallagents():
	query = usercol.find({'agentname' :{'$exists':True}})
	agentlist = [i['agentname'] for i in query]
	return agentlist





### Idea's for packaging to sell.....
### Sync Entire LDAP Database with Card Number and Socials into Separate MongoDB
## This way theres not need to have the ldap database all the time. --- Manual Sync as well as cron sync. 
## Also this way, LDAP is a module instead of a requirement. 

## Config File. 
## LDAP option
## MS Sharepoint Option
## Ability to turn on/off Card Scanning. 
## Ability to turn on/off last 5 of social.
## Ability to just allow manaul input. 
