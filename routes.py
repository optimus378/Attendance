from bottle import route, view, get, post, request, redirect, template, static_file
from datetime import datetime
import attendance
from ldap3 import Server, Connection, AUTO_BIND_NO_TLS, SUBTREE, ALL_ATTRIBUTES
import time
import os
import csv

### Class Management ###
@route('/admin/setclass')
@view('setclass')
def setclass():
       return dict( 
           title = 'Set Current Class:' , 
		   currentclass = attendance.readclass(),
		   todaydate = time.strftime('%m-%d-%Y'),
		   class_status = ''
           )

@post('/admin/setclass')
@view('setclass')
def setclassfuncs():
	if request.forms.get('classname'):
		currentclass = request.forms.get('classname')
		setclassresult = attendance.setclass(currentclass)
		if setclassresult is False:
			return template ('setclass.tpl' , currentclass = attendance.readclass(), class_status = "End the current Class before setting new Class" , todaydate = time.strftime('%m-%d-%Y'))
		else:
			return template ('setclass.tpl' , currentclass = attendance.readclass(), todaydate = time.strftime('%m-%d-%Y'), class_status = '')
	else:
		if attendance.endclass() is False:
			return template('setclass.tpl' , currentclass = attendance.readclass(), todaydate = time.strftime('%m-%d-%Y'), class_status = 'Class Ended- Nothing to Record')
		else:
			return template('setclass.tpl' , currentclass = attendance.readclass(), todaydate = time.strftime('%m-%d-%Y'), class_status = 'Class Ended')

### Attendance Page
@route('/')
@view('takeattendance')
def takeattendance():
	 return dict( 
           status='Ready',
		   currentclass = attendance.readclass(),
		   todaydate = time.strftime('%m-%d-%Y')
           )

@post('/')
@view('takeattendance')
def do_takeattendance():
	userinput = request.forms.get('userinput')
	classname = attendance.readclass()
	if classname is False:
		return template('takeattendance.tpl', status = "No class in session",todaydate = time.strftime('%m-%d-%Y'),currentclass = attendance.readclass())
	else:
		if len(userinput) == 20:
			searchkey='homePhone='
			inputtype='card'
			output= attendance.usercheck(searchkey, userinput, inputtype)
			return template('takeattendance.tpl', status = output, currentclass = attendance.readclass(), todaydate = time.strftime('%m-%d-%Y'))
		elif len(userinput) < 5:
			return template('takeattendance.tpl', status = "Error! Five digits please!",todaydate = time.strftime('%m-%d-%Y'),currentclass = attendance.readclass())
		elif len(userinput) > 5 and len(userinput) < 20:
			output = 'Error! Too many Digits. Last FIVE digits please.'
			return template('takeattendance.tpl', status = output, currentclass = attendance.readclass(), todaydate = time.strftime('%m-%d-%Y'))
		elif len(userinput) == 5:
			inputstatus = 'Social Entered'
			searchkey='pager='
			inputtype='social'
			cardninput = False
			output= attendance.usercheck(searchkey, userinput, inputtype)
			return template('takeattendance.tpl', status = output, currentclass = attendance.readclass(),todaydate = time.strftime('%m-%d-%Y'))

@route('/manualinput')
@view('manualinput')
def manualinput():
	 return dict(
           status='Getting Manual Input',
		   currentclass = attendance.readclass(),
		   todaydate = time.strftime('%m-%d-%Y')
           )
@post('/manualinput')
@view('manualinput')
def getmanualname():
	classname = attendance.readclass()
	if classname is False:
		return template('takeattendance.tpl', status = "No class in session",todaydate = time.strftime('%m-%d-%Y'),currentclass = attendance.readclass())
	else:
		userinput=request.forms.get('userinput')
		output = attendance.manualinput(userinput)
		return template('takeattendance.tpl', status = output, currentclass = attendance.readclass(), todaydate = time.strftime('%m-%d-%Y'))

@route('/admin')
@route('/admin/')
@view('reports')
def reports():
	return dict(
			currentclass = attendance.readclass(),
			todaydate = time.strftime('%m-%d-%Y'),
			currentreport = attendance.currentclassreport(),
			currentagentcount = attendance.countcurrentclass(),
			classlist = attendance.getclasslist(),
			notfound = None
			)
@post('/admin')
def deleteclass():
	classname = request.POST['classname']
	attendance.deleteclass(classname)
	return template('reports.tpl',
			currentclass = attendance.readclass(),
			todaydate = time.strftime('%m-%d-%Y'),
			currentreport = attendance.currentclassreport(),
			currentagentcount = attendance.countcurrentclass(),
			classlist = attendance.getclasslist(),
			notfound = None
			)


@route('/admin/reports/agents/<name>')
def classreport(name='name'):
	agentreport = attendance.getagentstats(name)
	return template('userreport.tpl', name=name, agentreport = agentreport,)

@post('/admin/reports/agentreport')
def agentreportsearch():
	agent = request.POST['agentname']
	agentreport = attendance.getagentstats(agent)
	if agentreport is not None:
		return template('userreport.tpl', name=agent, agentreport = agentreport)
	else:
		return template('reports.tpl',currentclass = attendance.readclass(),
			todaydate = time.strftime('%m-%d-%Y'),
			currentreport = attendance.currentclassreport(),
			currentagentcount = attendance.countcurrentclass(),
			classlist = attendance.getclasslist(),
			notfound = "Agent Not Found")

@route('/admin/reports/classes/<classname>')
def classreportsearch(classname = 'classname'):
	classreport = attendance.getclass_stats(classname)
	agentcount = attendance.countclass(classname)
	return template('classreport.tpl', name=classname, classreport = classreport, agentcount = agentcount)
	
### Add an Agent to a Single Class ##
@post('/admin/reports/class/manualagentadd')
def manualAgentAdd():
	agentname = request.POST['agentname']
	classname = request.POST['classname']
	attendance.manualAgentAdd(classname,agentname)
	classreport = attendance.getclass_stats(classname)
	agentcount = attendance.countclass(classname)
	return template('classreport.tpl', name=classname, classreport = classreport, agentcount = agentcount)

## Delete Agent from Single Class ##
@post('/admin/reports/classes/<classname>')
def delagentfromclass(classname='classname'):
	agentname = request.POST['agentname']
	attendance.delagentfromclass(classname,agentname)
	classreport = attendance.getclass_stats(classname)
	agentcount = attendance.countclass(classname)
	return template('classreport.tpl', name=classname, classreport = classreport, agentcount = agentcount)


@route('/admin/agentlist')
def listallagents():
	agentlist = attendance.listallagents()
	return template('agentlist.tpl', agentlist = agentlist)

### Download User Report ###
@route('/download/agents/<report:path>')
def pushtocsv(report = 'report'):
	attendance.agent_to_csv(report)
	return static_file(report + '.csv', root ='./static/temp', download=True)

### Download Class Report ###
@route('/download/classes/<report:path>')
def pushtocsv(report = 'report'):
	attendance.classtocsv(report)
	return static_file(report + '.csv', root ='./static/temp', download=True)
    
#@route('/reports)
#def search():
#    query = request.form['q']
#    text_results = db.command('text', 'posts', search=query, limit=SEARCH_LIMIT)
#    doc_matches = (res['obj'] for res in text_results['results'])
#    return render_template("search.html", results=results)

# -- REadbout Indexes and searchers here https://www.mongodb.com/blog/post/integrating-mongodb-text-search-with-a-python-app