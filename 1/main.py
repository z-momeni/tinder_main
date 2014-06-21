import flask, flask.views
import os
from flask_mail import Message,Mail
import functools
from neo4jrestclient.client import GraphDatabase
from neo4jrestclient.query import Q

app = flask.Flask(__name__)

app.secret_key = "1234"

gdb = GraphDatabase("http://localhost:7474/db/data/")
#gdbd = GraphDatabase("http://localhost:7474/db/data/")
#gdbw = GraphDatabase("http://localhost:7474/db/data/")
#gdbpro=GraphDatabase("http://localhost:7474/db/data/")
#gdbpro2=GraphDatabase("http://localhost:7474/db/data/")
#gdbf=GraphDatabase("http://localhost:7474/db/data/")


people = gdb.labels.create("People")		#label of user 
diaries = gdb.labels.create("Diaries")		#label of khaterat
wrote = gdb.labels.create("Wrote")		#label of relation between user and khaterat
lprofile = gdb.labels.create("Profile")	#label of profile user ha
myprofile = gdb.labels.create("Myprofile")	#label of relation between users and them profile 
friend = gdb.labels.create("Friend")		#label of relation between user and her friend

mail = Mail(app)


app.config["MAIL_SERVER"] = "smtp.gmail.com"
app.config["MAIL_PORT"] = 465
app.config["MAIL_USE_SSL"] = True
app.config["MAIL_USERNAME"] = 'happysnake.2014@gmail.com'
app.config["MAIL_PASSWORD"] = 'wormgame'

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
		q="""match (p:People { username : "%s"}) return p.password,p.year""" % user

		result = gdb.query(q=q)
		
		if (result[0][0]==passwd):
			flask.session['username'] = user
			return flask.redirect(flask.url_for('home'))
        	
         	flask.flash("Username doesn't exist or incorrect password")
        	return flask.redirect(flask.url_for('signin'))



#****************************************signup******************************************
class signup(flask.views.MethodView):
    def get(self):
        return flask.render_template('signup.html')
    
    def post(self):
	
	if 'reset' in flask.request.form:
		return flask.redirect(flask.url_for('signup'))
	
	user = flask.request.form['username']
	
	if 'send' in flask.request.form:
		
		if(flask.request.form['username']!="" and flask.request.form['password']!="" and flask.request.form['a-password']!="" and flask.request.form['mail']!="" and flask.request.form['year']!="" and flask.request.form['month']!="" and flask.request.form['day']
!=""):

			
			lookup = Q("username", exact=str(user))
			results = gdb.nodes.filter(lookup) 

			if len(results)!=0:
				flask.flash("your username is avilable.please change your username")
				print "your username is avilable.please change your username"
				return flask.redirect(flask.url_for('signup'))

			elif len(str(flask.request.form['password']))<=5:
				flask.flash("your password must more than 5 character")
				print "your password must more than 5 character"
				return flask.redirect(flask.url_for('signup'))

			elif flask.request.form['password']!=flask.request.form['a-password']:
				flask.flash("your password and confirm password is not equal ")
				print "your password and confirm password is not equal"
				return flask.redirect(flask.url_for('signup'))
			
			#elif (year<=0 or month<=0 or day<=0 or month>12 or day>31):
			#	print year ,month ,day
			#	flask.flash("your birthday's date is invalid ")
			#	print "your birthday's date is invalid"
			#	return flask.redirect(flask.url_for('signup'))


			else:
				flask.session['username'] = flask.request.form['username']

				#msg = Message("welcom to tinder group!",sender="happysnake.2014@gmail.com.com",recipients=["m.hajihosseini95@gmail.com"])
				#mail.send(msg)
				print "&&&&&&&&&&&&&&&&&&&"

				u = gdb.nodes.create(username =flask.request.form['username'],password = flask.request.form['password'],a_pssword=flask.request.form['a-password'],mail=flask.request.form['mail'],year=flask.request.form['year'],month=flask.request.form['month'],day=flask.request.form['day'])
				people.add(u)
				
				p = gdb.nodes.create(Id=user,firstname = '-' , lastname = '-' ,age ='-',gender='-', mail = flask.request.form['mail'] , country = '-',education='-',work='-',college='-',school='-' , biography = '-')
				lprofile.add(p)
				u.relationships.create("myprofile",p,Id=user)

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
		return flask.render_template('home.html')

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
			print "raft writing"
			return flask.redirect(flask.url_for('writing'))

		if "friends" in flask.request.form:
			print "user= ",user
			q="""match (p:People { username : "%s"})-[r:friend]-> (k:People) return k.username""" % user
			result = gdb.query(q=q)
			for r in result:
				print "result= ",r[0]
			return flask.redirect(flask.url_for('friends'))


#****************************************profile******************************************
class profile(flask.views.MethodView):
	@login_required
	def get(self):

		user = flask.session['username']
	
		q="""match (p:Profile { Id : "%s"}) return p.firstname,p.lastname,p.age,p.gender,p.mail,p.country,p.education,p.work,p.college,p.school,p.biography""" % user
		result = gdb.query(q=q)

		return flask.render_template('profile.html',firstname=result[0][0],lastname=result[0][1],age=result[0][2],gender ="female" ,mail=result[0][4],country=result[0][5],education = result[0][6],work = result[0][7],college = result[0][8],school = result[0][9],biography=result[0][10])

	@login_required
	def post(self):
		if "edit" in flask.request.form:
			return flask.redirect(flask.url_for('tanzimprofile'))


#****************************************friendprofile******************************************
class friendprofile(flask.views.MethodView):
	@login_required
	def get(self):

		ser = flask.session['txtsearch']
		
		q="""match (p:Profile { Id : "%s"}) return p.firstname,p.lastname,p.age,p.gender,p.mail,p.country,p.education,p.work,p.college,p.school,p.biography""" % ser
		result = gdb.query(q=q)

		return flask.render_template('friendprofile.html',firstname=result[0][0],lastname=result[0][1],age=result[0][2],gender ="female" ,mail=result[0][4],country=result[0][5],education = result[0][6],work = result[0][7],college = result[0][8],school = result[0][9],biography=result[0][10])


	@login_required
	def post(self):
				

		if "add" in flask.request.form:


			user = flask.session['username']
			ser = flask.session['txtsearch']
		
			
			q="""start n=node(*) match (p:People { username : "%s"})-[r:friend]-> (k:People) return k.username""" % user
			result = gdb.query(q=q)
			count=0
			print "len= ",len(result)
			print result
			for r in result:
				print "r= ",r[0]
				if r[0]==ser:
					count+=1

			print "count= ",count

			
			if (count==0):
				q="""MATCH (p:People{username:"%s"}),(q:People{username:"%s"}) CREATE (p)-[:friend]->(q) """ % (user,ser)
				result = gdb.query(q=q)

				return flask.redirect(flask.url_for('home'))	

			
			return flask.redirect(flask.url_for('home'))



#****************************************tanzimprofile******************************************
class tanzimprofile(flask.views.MethodView):
	@login_required
	def get(self):
		return flask.render_template('tanzimprofile.html')
	@login_required
	def post(self):
		if 'reset' in flask.request.form:
			return flask.redirect(flask.url_for('tanzimprofile'))
		
		user=flask.session['username']

		if 'send' in flask.request.form:

			q="""match (p:Profile { Id : "%s"}) set p.firstname="%s",p.lastname="%s",p.mail="%s",p.age="%s",p.country="%s",p.biography="%s",p.gender="%s",p.education="%s",p.work="%s",p.college="%s",p.school="%s" """ % (user,flask.request.form['firstname'],flask.request.form['lastname'],flask.request.form['mail'],flask.request.form['age'],flask.request.form['country'],flask.request.form['biography'],"female",flask.request.form['education'],flask.request.form['work'],flask.request.form['college'],flask.request.form['school'])
			result = gdb.query(q=q)
			
			return flask.redirect(flask.url_for('home'))			

			



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
				
				

				q="""MATCH (p:People{username:"%s"}) CREATE (d:Diaries{diarie:"%s"}) CREATE (p)-[:wrote]->(d) """ % (user,flask.request.form['text'])
				result = gdb.query(q=q)


				return flask.redirect(flask.url_for('test'))
		
			else:
				flask.flash("you must write date!")
				print("you must write date!")
				return flask.redirect(flask.url_for('writing'))

		if 'cancel' in flask.request.form:
			return flask.redirect(flask.url_for('writing'))



#****************************************mydiary******************************************
class mydiary(flask.views.MethodView):
	@login_required
	def get(self):
		return flask.render_template('mydiary.html')
	@login_required
	def post(self):
		return flask.render_template('mydiary.html')
	

#****************************************friends******************************************
class friends(flask.views.MethodView):
	@login_required
	def get(self):
		return flask.render_template('friends.html')
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

app.add_url_rule('/signin/home/friendprofile/',
                 view_func =  friendprofile.as_view('friendprofile'),
                 methods = ['GET','POST'])


app.add_url_rule('/signin/home/profile/tanzimprofile/',
                 view_func =  tanzimprofile.as_view('tanzimprofile'),
                 methods = ['GET','POST'])

app.debug = True
app.run()











