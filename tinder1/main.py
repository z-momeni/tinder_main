import flask, flask.views
import os
from flask.ext.mail import Mail, Message
#from flask_mail import Message,Mail
import functools
from neo4jrestclient.client import GraphDatabase
from neo4jrestclient.query import Q
from flask import Flask, render_template, request, redirect, url_for, send_from_directory
from werkzeug import secure_filename
#import flask_sijax
app = flask.Flask(__name__)
app.config.from_object(__name__)
mail = Mail(app)
app.secret_key = "1234"

gdb = GraphDatabase("http://localhost:7474/db/data/")

people = gdb.labels.create("People")		#label of user 
diaries = gdb.labels.create("Diaries")		#label of khaterat
wrote = gdb.labels.create("Wrote")		#label of relation between user and khaterat
friend = gdb.labels.create("Friend")		#label of relation between user and her friend

fdiaries = gdb.labels.create("Fdiaries")	#label of friend diaries
fridiaries = gdb.labels.create("Fridiaries")	#label of relation between user and friend diaries

public = gdb.labels.create("Public")		#label of public diaries
publicrel = gdb.labels.create("Publicrel")	#label of relation friend diaries

app.config['UPLOAD_FOLDER'] = '/home/malihe/tinder/test/tinder/static/img/media'
app.config['ALLOWED_EXTENSIONS'] = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

DEBUG = True
SECRET_KEY = 'hidden'
USERNAME = 'secret'
PASSWORD = 'secret'

MAIL_SERVER='imap.gmail.com'
MAIL_PORT=993
MAIL_USE_TLS = False
MAIL_USE_SSL= True
MAIL_USERNAME = 'happysnake.2014@gmail.com'
MAIL_PASSWORD = 'wormgame'

mail = Mail(app)
#app.config["MAIL_SERVER"] = "smtp.gmail.com"
#app.config["MAIL_PORT"] = 465
#app.config["MAIL_USE_SSL"] = True
#app.config["MAIL_USERNAME"] = 'happysnake.2014@gmail.com'
#app.config["MAIL_PASSWORD"] = 'wormgame'

class Main(flask.views.MethodView):
    def get(self):
        return flask.render_template('main.html')
    
    def post(self):
	if 'signin' in flask.request.form:
		return flask.redirect(flask.url_for('signin'))
	if 'signup' in flask.request.form:
		return flask.redirect(flask.url_for('signup'))

#****************************************signin******************************************
class signin(flask.views.MethodView):
    def get(self):
        return flask.render_template('signin.html')
    
    def post(self):
	
        user = flask.request.form['username']
        passwd = flask.request.form['password']
	if 'log in' in flask.request.form:
		q="""match (p:People { username : "%s"}) return p.password""" % user
		result = gdb.query(q=q)

		if (len(result)==0):
			print "your username is invalid!you must sign up."
			flask.flash("your username is invalid!you must sign up.")
        		return flask.redirect(flask.url_for('signup'))

		if (result[0][0]==passwd):
			flask.session['username'] = user
			return flask.redirect(flask.url_for('home'))
        	else:
         		flask.flash("your password is incorrect")
        		return flask.redirect(flask.url_for('signin'))


#****************************************email******************************************

def send_mail():
    msg = Message(
      'Hello',
       sender='happysnake.2014@gmail.com',
       recipients=
       ['m.hajihosseini95@gmail.com'])
    msg.body = "This is the email body"
    mail.send(msg)
    return "Sent"

#****************************************signup******************************************
class signup(flask.views.MethodView):
    def get(self):
        return flask.render_template('signup.html')
    
    def post(self):
	
	if 'reset' in flask.request.form:
		return flask.redirect(flask.url_for('signup'))
	
	user = flask.request.form['username']
	
	if 'send' in flask.request.form:

		if(flask.request.form['username']!="" and flask.request.form['password']!="" and flask.request.form['a_password']!="" and flask.request.form['mail']!="" and flask.request.form['year']!="" and flask.request.form['month']!="" and flask.request.form['day']
!=""):

			q="""match (p:People { username : "%s"}) return p.password""" % user
			results = gdb.query(q=q) 
			print "result",results,"len= ",len(results)
			if len(results)!=0:

				flask.flash("your username is repetitive.please change your username")
				print "your username is repetitive.please change your username"
				return flask.redirect(flask.url_for('signup'))

			elif len(str(flask.request.form['password']))<=5:

				flask.flash("your password must more than 5 character ! please change your password")
				print "your password must more than 5 character ! please change your password"
				return flask.redirect(flask.url_for('signup'))

			elif flask.request.form['password']!=flask.request.form['a_password']:

				flask.flash("your password and confirm password is not equal ")
				print "your password and confirm password is not equal"
				return flask.redirect(flask.url_for('signup'))
			
			#elif (year<=0 or month<=0 or day<=0 or month>12 or day>31):
				#print year ,month ,day
			#	flask.flash("your birthday's date is invalid ")
			#	print "your birthday's date is invalid"
			#	return flask.redirect(flask.url_for('signup'))


			else:
				flask.session['username'] = flask.request.form['username']

				#msg = Message("welcom to tinder group!",sender="happysnake.2014@gmail.com.com",recipients=["m.hajihosseini95@gmail.com"])
				#mail.send(msg)
				print "wwwwwww"
				print flask.request.form['username']
				print flask.request.form['password']
				print flask.request.form['a_password']
				print flask.request.form['year']
				print flask.request.form['month']
				print flask.request.form['day']
				print flask.request.form['mail']

				#q=""" create (s:People{username:"%s",password:"%s"}) """%(flask.request.form['username'],flask.request.form['password'])

				q=""" create (s:People{username:"%s",password:"%s",a_password:"%s",mail:"%s",year:"%s",month:"%s",day:"%s",firstname:"%s",lastname:"%s",age:"%s",gender:"%s",country:"%s",education:"%s",work:"%s",college:"%s",school:"%s",biography:"%s",imageaddress:"%s"}) """ %(flask.request.form['username'],flask.request.form['password'],flask.request.form['a_password'],flask.request.form['mail'],flask.request.form['year'],flask.request.form['month'],flask.request.form['day'],"-","-","-","-","-","-","-","-","-","-","/static/img/media/profile.jpg")

				result = gdb.query(q=q)
				
				
				if os.path.exists('/home/malihe/tinder/test/tinder/static/img/media/'+str(flask.request.form['username'])):
    					pass
				else:
    					os.mkdir('/home/malihe/tinder/test/tinder/static/img/media/'+str(flask.request.form['username']))
				return flask.redirect(flask.url_for('home'))
		

		else:
			flask.flash("you must fill all the blanks!")
		      	return flask.redirect(flask.url_for('signup'))



#**********************************************************************************

def login_required(method):
	@functools.wraps(method)
	def wrapper(*args,**kwargs):

		if 'username' in flask.session:

			return method(*args,**kwargs)
		else:
			print "A login is required to see the page!"
			flask.flash("A login is required to see the page!")
			return flask.redirect(flask.url_for('main'))
	return wrapper


#****************************************home******************************************

class home(flask.views.MethodView):
	@login_required
	def get(self):
						
		q="""match (k:People)-[r:fridiaries]-> (d:Diaries) return d.diarie ,d.writer,r.year , r.month , r.day ,r.title """ 
		result = gdb.query(q=q)
		
		dfriends=[]
		comments = ['a','b','c']
		for i in range(len(result)):
			x=dict([('text',result[i][0]),('user',result[i][1]),('year',result[i][2]) , ('month',result[i][3]) , ('day',result[i][4]) , ('title',result[i][5]) , ('feel',"laugh") , ('comment',comments),('tag',"yyyyyyyy")])
			dfriends.append(x)

		return flask.render_template('home.html',posts=dfriends)

	@login_required
	def post(self):
		user = flask.session['username']
		#print flask.request.form, 'submitsearch' in flask.request.form
		if "amenudiary" in flask.request.form:
			return flask.redirect(flask.url_for('mydiary'))

		if "btnmenusignout" in flask.request.form:
			flask.session.pop('username',None)
			return flask.redirect(flask.url_for('main'))

		if "amenuhome" in flask.request.form:
			return flask.redirect(flask.url_for('home'))
		
		if "amenuprofile" in flask.request.form:
			#print "raft tosh"
			return flask.redirect(flask.url_for('profile'))

		if "amenuabout" in flask.request.form:
			return flask.redirect(flask.url_for('welcome'))

		if "submitsearch" in flask.request.form:
			flask.session['txtsearch']=flask.request.form['txtsearch']
			return flask.redirect(flask.url_for('friendprofile'))

		if "aarchive " in flask.request.form:
			return flask.redirect(flask.url_for('writing'))


		if "settings" in flask.request.form:
			return flask.redirect(flask.url_for('settings'))

		if "friends" in flask.request.form:

			#q="""match (p:People { username : "%s"})-[r:friend]-> (k:People) return k.username""" % user
			#result = gdb.query(q=q)
			#for r in result:
			#	print "result= ",r[0]
			return flask.redirect(flask.url_for('friends'))


#****************************************profile******************************************
class profile(flask.views.MethodView):
	@login_required
	def get(self):

		user = flask.session['username']
	
		q="""match (p:People { username : "%s"}) return p.firstname,p.lastname,p.age,p.gender,p.mail,p.country,p.education,p.work,p.college,p.school,p.biography , p.imageaddress""" % user
		result = gdb.query(q=q)

		return flask.render_template('profile.html',firstname=result[0][0],lastname=result[0][1],age=result[0][2],gender =result[0][3] ,mail=result[0][4],country=result[0][5],education = result[0][6],work = result[0][7],college = result[0][8],school = result[0][9],biography=result[0][10],filename=result[0][11])

	@login_required
	def post(self):
		pass

#****************************************friendprofile******************************************
class friendprofile(flask.views.MethodView):
	@login_required
	def get(self):

		ser = flask.session['txtsearch']
		
		q="""match (p:People { username : "%s"}) return p.firstname,p.lastname,p.age,p.gender,p.mail,p.country,p.education,p.work,p.college,p.school,p.biography""" % ser
		result = gdb.query(q=q)
		if len(result)==0:
			print "this username is invalid"
			flask.flash("this username is invalid")
			return flask.render_template('home.html')
		return flask.render_template('friendprofile.html',firstname=result[0][0],lastname=result[0][1],age=result[0][2],gender =result[0][3] ,mail=result[0][4],country=result[0][5],education = result[0][6],work = result[0][7],college = result[0][8],school = result[0][9],biography=result[0][10])


	@login_required
	def post(self):
				

		if "add" in flask.request.form:

			user = flask.session['username']
			ser = flask.session['txtsearch']
		
			q="""start n=node(*) match (p:People { username : "%s"})-[r:friend]-> (k:People) return k.username""" % user
			result = gdb.query(q=q)
			count=0
			for r in result:
				if r[0]==ser:
					count+=1

			if (count==0):
				q="""MATCH (p:People{username:"%s"}),(q:People{username:"%s"}) CREATE (p)-[:friend]->(q) """ % (user,ser)
				result = gdb.query(q=q)

				return flask.redirect(flask.url_for('home'))	

			
			return flask.redirect(flask.url_for('home'))


#****************************************upload******************************************

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in app.config['ALLOWED_EXTENSIONS']


def upload():
	print "lllllllllmmmmm" 
	user = flask.session['username']
	print "user:        ",user
    	f = flask.request.files['file']
	print "sssssssssssssssss= ",f.filename
    	if f and allowed_file(f.filename):
        	filename = secure_filename(f.filename)
	
       		f.save(os.path.join(app.config['UPLOAD_FOLDER']+"/"+str(user), filename))
        	#return flask.redirect(url_for('profile'))

#def uploaded_file(filename):
#	return send_from_directory(app.config['UPLOAD_FOLDER'],
 #                              filename)

#****************************************tanzimprofile******************************************
#entekhab kone email ro bebinan  
class tanzimprofile(flask.views.MethodView):
	@login_required
	def get(self):
		user = flask.session['username']
		q="""match (p:People { username : "%s"}) return p.firstname,p.lastname,p.age,p.gender,p.mail,p.country,p.education,p.work,p.college,p.school,p.biography , p.imageaddress""" % user
		result = gdb.query(q=q)
		print "wwwwwwwwwwwwwww= ",result[0][0]
		return flask.render_template('tanzimprofile.html',firstname=result[0][0],lastname=result[0][1],age=result[0][2],gender =result[0][3] ,mail=result[0][4],country=result[0][5],education = result[0][6],work = result[0][7],college = result[0][8],school = result[0][9],biography=result[0][10],filename=result[0][11])


	@login_required
	def post(self):
		user = flask.session['username']
		if 'remove image'in flask.request.form :
			q="""match (p:People { username : "%s"}) set p.imageaddress="%s" """ % (user,"/static/img/media/profile.jpg")
			result = gdb.query(q=q)
			return flask.redirect(flask.url_for('profile'))			
		
		if 'reset' in flask.request.form:
			return flask.redirect(flask.url_for('tanzimprofile'))
		


		if 'send' in flask.request.form:
					
			f = flask.request.files['file']

			if (f.filename != ""):
				addres = "/static/img/media/" + str(user) +"/"+ str(f.filename)
				q="""match (p:People { username : "%s"}) set p.imageaddress="%s" """ % (user,addres)
				result = gdb.query(q=q)

	    			if f and allowed_file(f.filename):
					filename = secure_filename(f.filename)
	
		       		f.save(os.path.join(app.config['UPLOAD_FOLDER']+"/"+str(user), filename))
				f.close()
			a=[flask.request.form['firstname'],flask.request.form['lastname'],flask.request.form['mail'],flask.request.form['age'],flask.request.form['country'],flask.request.form['biography'],flask.request.form['education'],flask.request.form['work'],flask.request.form['college'],flask.request.form['school'],flask.request.form['male']]			

			if (a[2]!="" and (a[10]=="female" or a[10]=="male")):
				for i in range(11):
					if a[i]=="":
						a[i]="--"


				q="""match (p:People { username : "%s"}) set p.firstname="%s",p.lastname="%s",p.mail="%s",p.age="%s",p.country="%s",p.biography="%s",p.gender="%s",p.education="%s",p.work="%s",p.college="%s",p.school="%s" """ % (user,a[0],a[1],a[2],a[3],a[4],a[5],a[10],a[6],a[7],a[8],a[9])
				result = gdb.query(q=q)
				return flask.redirect(flask.url_for('profile'))			
			else:
				flask.flash("you must enter your mail")
				print "you must enter your mail"
				return flask.redirect(flask.url_for('tanzimprofile'))			


#****************************************writing******************************************

class writing(flask.views.MethodView):
	@login_required
	def get(self):
		return flask.render_template('writing.html')

	@login_required
	def post(self):
		y = flask.request.form['year']
		m = flask.request.form['month']
		da = flask.request.form['day']
		titl = flask.request.form['title']
		user=flask.session['username']
		
		if 'save' in flask.request.form:
			
			if (y!="" and m!="" and da!=""):
				if flask.request.form['privacy']=="private":

					q="""MATCH (p:People{username:"%s"}) CREATE (d:Diaries{diarie:"%s",writer:"%s"}) CREATE (p)-[:wrote{year:"%s",month:"%s",day:"%s",title:"%s"}]->(d) """ % (user,flask.request.form['text'],user,y,m,da,titl)
					result = gdb.query(q=q)
				


				if flask.request.form['privacy']=="friends":

					q="""MATCH (p:People{username:"%s"}) CREATE (d:Diaries{diarie:"%s",writer:"%s"}) CREATE (p)-[:wrote{year:"%s",month:"%s",day:"%s",title:"%s"}]->(d) """ % (user,flask.request.form['text'],user,y,m,da,titl)
					result = gdb.query(q=q)
				

					q="""MATCH (p:People{username:"%s"})-[r:friend]-> (k:People) return k.username """ % (user)
					results = gdb.query(q=q)
					
					if (len(results)!=0):
						#q=""" create (r:Fdiaries{diarie:"%s",writer:"%s"}) """ %(flask.request.form['text'],user) 
						#result = gdb.query(q=q)

						for i in range(len(results)):
							print results[i][0]
							#q="""MATCH (p:People {username:"%s"}),(d:Fdiaries{diarie:"%s",writer:"%s"})  CREATE (p)-[:fridiaries{year:"%s",month:"%s",day:"%s",titile:"%s"}]->(d) """ % (results[i][0],flask.request.form['text'],y,m,da,titl)
							q="""MATCH (p:People {username:"%s"}),(d:Diaries{diarie:"%s",writer:"%s"})  CREATE (p)-[:fridiaries{year:"%s",month:"%s",day:"%s",title:"%s"}]->(d) """ % (results[i][0],flask.request.form['text'],user,y,m,da,titl)
							results1 = gdb.query(q=q)




				if flask.request.form['privacy']=="public":

					q="""MATCH (p:People{username:"%s"}) CREATE (d:Diaries{diarie:"%s",writer:"%s"}) CREATE (p)-[:wrote{year:"%s",month:"%s",day:"%s",title:"%s"}]->(d) """ % (user,flask.request.form['text'],user,y,m,da,titl)
					result = gdb.query(q=q)


				


					q="""MATCH (p:People{username:"%s"})-[r:friend]-> (k:People) return k.username """ % (user)
					results = gdb.query(q=q)
					print "len= ",len(results)
					if (len(results)!=0):
						#q=""" create (r:Fdiaries{diarie:"%s",writer:"%s"}) """ %(flask.request.form['text'],user) 
						#result = gdb.query(q=q)

						for i in range(len(results)):
							print "!1111111111",results[i][0]
							print results[i][0]
							q="""MATCH (p:People {username:"%s"}),(d:Diaries{diarie:"%s",writer:"%s"})  CREATE (p)-[:fridiaries{year:"%s",month:"%s",day:"%s",title:"%s"}]->(d) """ % (results[i][0],flask.request.form['text'],user,y,m,da,titl)
							results1 = gdb.query(q=q)





					#q=""" create (r:Public{diarie:"%s",writer:"%s"}) """ %(flask.request.form['text'],user) 
					#result = gdb.query(q=q)

					q="""MATCH (p:People) return p.username """ 
					result = gdb.query(q=q)

					for i in range(len(result)):
						print result[i][0]
						q="""MATCH (p:People {username:"%s"}),(d:Diaries{diarie:"%s",writer:"%s"})  CREATE (p)-[:publicrel{year:"%s",month:"%s",day:"%s",title:"%s"}]->(d) """ % (result[i][0],flask.request.form['text'],user,y,m,da,titl)
						results = gdb.query(q=q)
				return flask.redirect(flask.url_for('writing'))
		
			else:
				flask.flash("you must write date!")
				print("you must write date!")
				return flask.redirect(flask.url_for('writing'))
				
#		if 'tag' in flask.request.form:
#			q="""MATCH (p:People{username:"%s"}) CREATE (d:Diaries{diarie:"%s"}) CREATE (p)-[:wrote{year:"%s",month:"%s",day:"%s",titile:"%s"}]->(d) """ % (user,flask.request.form['text'],y,m,da,titl)
#			result = gdb.query(q=q)
			
#			q="""MATCH (p:People{username:"%s"})-[r:friend]-> (k:People) return k.username """ % (user)
#			result = gdb.query(q=q)
#			d = gdb.nodes.create(diarie=flask.request.form['text'])
#			frienddiaries.add(d)

		if 'cancel' in flask.request.form:
			return flask.redirect(flask.url_for('writing'))


#****************************************mydiary******************************************
class mydiary(flask.views.MethodView):
	@login_required
	def get(self):
		return flask.render_template('mydiary.html')
	@login_required
	def post(self):
		if 'march' or 'april' or 'may' or 'june' or 'july' or 'august' or 'september' or 'octobr' or 'november' or 'desember' or 'januery' or 'febuery' in flask.request.form:
 			return flask.redirect(flask.url_for('diary'))
		#return flask.render_template('mydiary.html')
	


#****************************************diary******************************************
class diary(flask.views.MethodView):
	@login_required
	def get(self):
		user = flask.session['username']
		q="""match (k:People{username:"%s"})-[r:wrote]-> (d:Diaries) return d.diarie ,d.writer,r.year , r.month , r.day ,r.title """%user 
		result = gdb.query(q=q)
		
		diary=[]
		comments = ['a','b','c']
		for i in range(len(result)):
			x=dict([('text',result[i][0]),('user',result[i][1]),('year',result[i][2]) , ('month',result[i][3]) , ('day',result[i][4]) , ('title',result[i][5]) , ('feel',"laugh") , ('comment',comments),('tag',"yyyyyyyy")])
			diary.append(x)
		return flask.render_template('diary.html',posts=diary)
	@login_required
	def post(self):
		return flask.render_template('diary.html')
	


#****************************************friends******************************************
class friends(flask.views.MethodView):
	@login_required
	def get(self):
		user = flask.session['username']
		q="""match (p:People { username : "%s"})-[r:friend]-> (k:People) return k.firstname,k.lastname,k.imageaddress """ % user
		result = gdb.query(q=q)
		friends=[]

		for i in range(len(result)):
			x=dict([('firstname',result[i][0]),('lastname',result[i][1]),('images',result[i][2])])
			friends.append(x)
		for friend in friends:
			print friend['firstname']
		print "friends",friends
		return flask.render_template('friends.html',friends = friends)
	@login_required
	def post(self):

		return flask.render_template('friends.html')
	


#****************************************welcome******************************************
class welcome(flask.views.MethodView):
	@login_required
	def get(self):
		return flask.render_template('welcome.html')
	@login_required
	def post(self):
		return flask.render_template('welcome.html')

#****************************************settings******************************************

class settings(flask.views.MethodView):
	def get(self):
		return flask.render_template('settings.html')
	@login_required
	def post(self):
		if 'save' in flask.request.form:
			user = flask.session['username']
			print "user= ",user
			oldpass = flask.request.form['oldpass']
			newpass = flask.request.form['newpass']
			confirmpass = flask.request.form['confirmpass']

			q="""MATCH (p:People{username:"%s"}) return p.password  """ % (user)
			result=gdb.query(q=q)

			if (result[0][0]==oldpass) and (newpass==confirmpass):
				print "11111111111111111111111111"
				q="""MATCH (p:People{username:"%s"}) set p.password="%s" ,p.a_pssword="%s" """ % (user,newpass,confirmpass)
				result=gdb.query(q=q)
			return flask.redirect(flask.url_for('home'))


#****************************************public******************************************

class public(flask.views.MethodView):
	@login_required
	def get(self):

		q="""match (k:People)-[r:publicrel]-> (d:Diaries) return d.diarie ,d.writer,r.year , r.month , r.day ,r.title """ 
		result = gdb.query(q=q)
		
		publics=[]
		comments = ['a','b','c']
		for i in range(len(result)):
			x=dict([('text',result[i][0]),('user',result[i][1]),('year',result[i][2]) , ('month',result[i][3]) , ('day',result[i][4]) , ('title',result[i][5]) , ('feel',"laugh") , ('comment',comments)])
			publics.append(x)
		return flask.render_template('public.html',posts=publics)
	@login_required
	def post(self):
		return flask.render_template('public.html')


#****************************************test******************************************
class test(flask.views.MethodView):
	@login_required
	def get(self):
		return flask.render_template('test.html')
	@login_required
	def post(self):
		return flask.render_template('test.html')

app.add_url_rule('/',
                 view_func =  Main.as_view('main'),
                 methods = ['GET','POST'])


app.add_url_rule('/signin/',
		view_func = signin.as_view('signin'),
		methods = ['GET','POST'])

app.add_url_rule('/signup/',
		view_func = signup.as_view('signup'),
		methods = ['GET','POST'])

app.add_url_rule('/signin/home/',
                 view_func =  home.as_view('home'),
                 methods = ['GET','POST'])

app.add_url_rule('/signin/home/writing/',
                 view_func =  writing.as_view('writing'),
                 methods = ['GET','POST'])

app.add_url_rule('/signin/home/writing/test/',
                 view_func =  test.as_view('test'),
                 methods = ['GET','POST'])

app.add_url_rule('/signin/home/welcome/',
                 view_func =  welcome.as_view('welcome'),
                 methods = ['GET','POST'])

app.add_url_rule('/signin/home/profile/',
                 view_func =  profile.as_view('profile'),
                 methods = ['GET','POST'])

app.add_url_rule('/signin/home/friends/',
                 view_func =  friends.as_view('friends'),
                 methods = ['GET','POST'])

app.add_url_rule('/signin/home/mydiary/',
                 view_func =  mydiary.as_view('mydiary'),
                 methods = ['GET','POST'])

app.add_url_rule('/signin/home/mydiary/diary/',
                 view_func =  diary.as_view('diary'),
                 methods = ['GET','POST'])

app.add_url_rule('/signin/home/friendprofile/',
                 view_func =  friendprofile.as_view('friendprofile'),
                 methods = ['GET','POST'])

app.add_url_rule('/signin/home/settings/',
                 view_func =  settings.as_view('settings'),
                 methods = ['GET','POST'])

app.add_url_rule('/signin/home/public/',
                 view_func =  public.as_view('public'),
                 methods = ['GET','POST'])


app.add_url_rule('/signin/home/profile/tanzimprofile/',
                 view_func =  tanzimprofile.as_view('tanzimprofile'),
                 methods = ['GET','POST'])

#app.add_url_rule('/signin/home/profile/tanzimprofile/profile',
#                 view_func =  profile.as_view('profile'),
#                 methods = ['GET','POST'])

#app.add_url_rule('/signin/home/profile/tanzimprofile/upload/',
#                 view_func =  upload.as_view('upload'),
#	         methods = ['GET','POST'])


app.debug = True
app.run()











