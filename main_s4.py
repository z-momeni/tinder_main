import flask, flask.views
import os
from flask_mail import Message,Mail
import functools
from neo4jrestclient.client import GraphDatabase
from neo4jrestclient.query import Q

app = flask.Flask(__name__)

app.secret_key = "1234"

gdbp = GraphDatabase("http://localhost:7474/db/data/")
gdbd = GraphDatabase("http://localhost:7474/db/data/")
gdbw = GraphDatabase("http://localhost:7474/db/data/")
gdbpro=GraphDatabase("http://localhost:7474/db/data/")
gdbpro2=GraphDatabase("http://localhost:7474/db/data/")

people = gdbp.labels.create("People")		#label of user 
diaries = gdbd.labels.create("Diaries")		#label of khaterat
wrote = gdbw.labels.create("Wrote")		#label of relation between user and khaterat
profile = gdbpro.labels.create("Profile")	#label of profile user ha
myprofile = gdbpro2.labels.create("Myprofile")	#label of relation between users and them profile 

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


class signin(flask.views.MethodView):
    def get(self):
        return flask.render_template('signin.html')
    
    def post(self):
	#global user	
        #required = ['username','password']
	#for r in required:
	#        if r not in flask.request.form:
        #      		flask.flash("Error: {0} is required.".format(r))#nafahmidim
        #        	return flask.redirect(flask.url_for('signin'))


        user = flask.request.form['username']
        passwd = flask.request.form['password']

	if 'log in' in flask.request.form:
		q = """start n=node(*) return n"""
		lookup = Q("username", exact=str(user))
		results = gdbp.nodes.filter(lookup)
		print len(results)
 
		for i in range(len(results)):
			n = gdbp.node[results[i].id]
			if n["password"]==passwd:
				flask.session['username'] = user
				print n.username
				return flask.redirect(flask.url_for('home'))
        	
         	flask.flash("Username doesn't exist or incorrect password")
        	return flask.redirect(flask.url_for('signin'))




class signup(flask.views.MethodView):
    def get(self):
        return flask.render_template('signup.html')
    
    def post(self):
	
	if 'reset' in flask.request.form:
		return flask.redirect(flask.url_for('signup'))
	
	user = flask.request.form['username']
	password = flask.request.form['password']
	a_password = flask.request.form['a-password']
	mail = flask.request.form['mail']
	year = flask.request.form['year']
	month = flask.request.form['month']
	day = flask.request.form['day']


	if 'send' in flask.request.form:
		
		if(user!="" and password!="" and a_password!="" and mail!="" and year!="" and month!="" and day!=""):

			q = """start n=node(*) return n"""
			lookup = Q("username", exact=str(user))
			results = gdbp.nodes.filter(lookup) 

			if len(results)!=0:
				flask.flash("your username is avilable.please change your username")
				print "your username is avilable.please change your username"
				return flask.redirect(flask.url_for('signup'))

			elif len(str(password))<=5:
				flask.flash("your password must more than 5 character")
				print "your password must more than 5 character"
				return flask.redirect(flask.url_for('signup'))

			elif password!=a_password:
				flask.flash("your password and confirm password is not equal ")
				print "your password and confirm password is not equal"
				return flask.redirect(flask.url_for('signup'))
			
			#elif (year<=0 or month<=0 or day<=0 or month>12 or day>31):
			#	print year ,month ,day
			#	flask.flash("your birthday's date is invalid ")
			#	print "your birthday's date is invalid"
			#	return flask.redirect(flask.url_for('signup'))


			else:
				flask.session['username'] = user

				msg = Message("welcom to tinder group!",
                  sender="happysnake.2014@gmail.com.com",
                  recipients=["m.hajihosseini95@gmail.com"])
				#mail.send(msg)

				u = gdbp.nodes.create(username =flask.request.form['username'],password = flask.request.form['password'],a_pssword=flask.request.form['a-password'],mail=flask.request.form['mail'],year=flask.request.form['year'],month=flask.request.form['month'],day=flask.request.form['day'])
				people.add(u)
				
				p=gdbpro.nodes.create(Id=user,firstname = ' ' , lastname = ' ' , email = ' ' , age = ' ' , country = ' ' , biography = ' ')
				profile.add(p)
				u.relationships.create("myprofile",p,Id=user)

				return flask.redirect(flask.url_for('home'))
		

		else:
			flask.flash("you must fill all the blanks!")
		      	return flask.redirect(flask.url_for('signup'))


def login_required(method):
	@functools.wraps(method)
	def wrapper(*args,**kwargs):

		if 'username' in flask.session:
			#print user
			return method(*args,**kwargs)
		else:
			print "A login is required to see the page!"
			flask.flash("A login is required to see the page!")
			return flask.redirect(flask.url_for('main'))
	return wrapper

class tanzimprofile(flask.views.MethodView):
	@login_required
	def get(self):
		return flask.render_template('tanzimprofile.html')
	@login_required
	def post(self):
		if 'reset' in flask.request.form:
			return flask.redirect(flask.url_for('tanzimprofile'))
		
		#First=flask.request.form['firstname']
		#Last=flask.request.form['lastname']
		#Email=flask.request.form['email']
		#Age=flask.request.form['aga']
		#Country=flask.request.form['country']
		#Biography=flask.request.form['biography']
		user=flask.session['username']

		#be nazaram oon jayi ke dare signup mishe bayad node profile khali sakhte she inja propertie hash por she .
		if 'send' in flask.request.form:
			print "**************"

			q = """start n=node(*) return n"""
			lookup = Q("Id", exact=str(user))
			results = gdbpro.nodes.filter(lookup) 
			print "###########"
			print len(results)
			for i in range(len(results)):
				n = gdbpro.node[results[i].id]
				n['firstname']=flask.request.form['firstname']
				n['lastname']=flask.request.form['lastname']
				n['email']=flask.request.form['email']
				n['age']=flask.request.form['age']
				n['country']=flask.request.form['country']
				n['biography']=flask.request.form['biography']
				print flask.request.form['biography']
				print "'^^^^^^^^^^^^^^^^^^"
			return flask.redirect(flask.url_for('home'))			


class writing(flask.views.MethodView):
	@login_required
	def get(self):
		return flask.render_template('writing.html')

	@login_required
	def post(self):
		y = flask.request.form['year']
		m = flask.request.form['month']
		da = flask.request.form['day']
		user=flask.session['username']

		if 'save' in flask.request.form:

			if (y!="" and m!="" and da!=""):
				d=gdbd.nodes.create(diarie=flask.request.form['table'])
				diaries.add(d)
				q = """start n=node(*) return n"""
				lookup = Q("username", exact=str(user))
				results = gdbp.nodes.filter(lookup) 
				#print len(results)
				for i in range(len(results)):
					#print len(results)
					n = gdbp.node[results[i].id]
					#print n.id
					n.relationships.create("wrote",d,year=y,month=m,day=da)
			
			#q = """start n=node(*) return n"""
			#q = """start n=node(*) match (n)-[:knows]-(b) return b `"""
			#lookup = Q("address", exact=str(user))
			#results = gdb.query(q, returns=(client.Node, unicode, client.Relationship))
			#results = gdb.query(q=q)			
			#results = gdb.nodes.filter(lookup) 
			#n = gdb.node[results[0].id]
			#n['diari']=flask.request.form['table']
	
				return flask.redirect(flask.url_for('test'))
		
			else:
				flask.flash("you must write date!")
				print("you must write date!")
				return flask.redirect(flask.url_for('writing'))

		if 'log out' in flask.request.form:
			flask.session.pop('username',None)
			return flask.redirect(flask.url_for('main'))
	


class test(flask.views.MethodView):
	@login_required
	def get(self):
		return flask.render_template('test.html')
	@login_required
	def post(self):
		return flask.render_template('test.html')

class home(flask.views.MethodView):
	@login_required
	def get(self):
		return flask.render_template('home.html')

	@login_required
	def post(self):

		if 'sign out' in flask.request.form:
			flask.session.pop('username',None)
			return flask.redirect(flask.url_for('main'))

		if 'home' in flask.request.form:
			return flask.redirect(flask.url_for('home'))
		
		if 'profile' in flask.request.form:
			flask.flash("raft tosh")
			print "raft tosh"
			return flask.redirect(flask.url_for('tanzimprofile'))

		if 'about us' in flask.request.form:
			return flask.redirect(flask.url_for('welcome'))

		if 'search' in flask.request.form:
			print "@@@@@@@@@@@"
			ser = flask.request.form['search']
			q = """start n=node(*) return n"""
			lookup = Q("Id" , exact = str(ser))
			result = gdbpro.nodes.filter(lookup)
			n=gdbpro.node[results[0].id]
			print n['firstname']
			print n['lastname']
			#print "@@@@@@@@@@@"
			return flask.redirect(flask.url_for('welcome'))

		if 'archive' in flask.request.form:
			print "raft writing"
			return flask.redirect(flask.url_for('writing'))


class welcome(flask.views.MethodView):
	@login_required
	def get(self):
		return flask.render_template('welcome.html')
	@login_required
	def post(self):
		return flask.render_template('welcome.html')


		


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

app.add_url_rule('/signin/home/tanzimprofile/',
                 view_func =  tanzimprofile.as_view('tanzimprofile'),
                 methods = ['GET','POST'])


#app.add_url_rule('/signin/test/',
#		view_func = test.as_view('test'),
#		methods = ['GET','POST'])

app.debug = True
app.run()











