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
gdbf=GraphDatabase("http://localhost:7474/db/data/")


people = gdbp.labels.create("People")		#label of user 
diaries = gdbd.labels.create("Diaries")		#label of khaterat
wrote = gdbw.labels.create("Wrote")		#label of relation between user and khaterat
lprofile = gdbpro.labels.create("Profile")	#label of profile user ha
myprofile = gdbpro2.labels.create("Myprofile")	#label of relation between users and them profile 
friend = gdbf.labels.create("Friend")		#label of relation between user and her friend

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
				
				p=gdbpro.nodes.create(Id=user,firstname = '-' , lastname = '-' ,age ='-',gender='-', mail = flask.request.form['mail'] , country = '-',education='-',work='-',college='-',school='-' , biography = '-')
				lprofile.add(p)
				u.relationships.create("myprofile",p,Id=user)

				return flask.redirect(flask.url_for('home'))
		

		else:
			flask.flash("you must fill all the blanks!")
		      	return flask.redirect(flask.url_for('signup'))


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



class home(flask.views.MethodView):
	@login_required
	def get(self):
		return flask.render_template('home.html')

	@login_required
	def post(self):
		#print flask.request.form, 'submitsearch' in flask.request.form
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


class profile(flask.views.MethodView):
	@login_required
	def get(self):

		user = flask.session['username']
		q="""start n=node(*) return n"""
		lookup = Q("Id" , exact=str(user))
		result = gdbpro.nodes.filter(lookup)
		n = gdbpro.node[result[0].id]

		return flask.render_template('profile.html',firstname=n['firstname'],lastname=n['lastname'],age=n['age'],gender ="female" ,mail=n['mail'],country=n['country'],education = n['education'],work = n['work'],college = n['college'],school = n['school'],biography=n['biography'])
	
	@login_required
	def post(self):
		if "edit" in flask.request.form:
			return flask.redirect(flask.url_for('tanzimprofile'))


class friendprofile(flask.views.MethodView):
	@login_required
	def get(self):

		ser = flask.session['txtsearch']
		q="""start n=node(*) return n"""
		lookup = Q("Id" , exact=str(ser))
		result = gdbpro.nodes.filter(lookup)
		n = gdbpro.node[result[0].id]
		
		return flask.render_template('friendprofile.html',firstname=n['firstname'],lastname=n['lastname'],age=n['age'],gender ="female" ,mail=n['mail'],country=n['country'],education = n['education'],work = n['work'],college = n['college'],school = n['school'],biography=n['biography'])

	@login_required
	def post(self):
		if "add" in flask.request.form:
			user = flask.session['username']
			ser = flask.session['txtsearch']

			q="""start n=node(*) return n"""
			lookup = Q("username" , exact=str(ser))
			result = gdbp.nodes.filter(lookup)
			n = gdbp.node[result[0].id]
			
			q="""start n=node(*) return n"""
			lookup = Q("username" , exact=str(user))
			result = gdbp.nodes.filter(lookup)
			u = gdbp.node[result[0].id]
			u.relationships.create("friend",n)

			return flask.redirect(flask.url_for('home'))



class tanzimprofile(flask.views.MethodView):
	@login_required
	def get(self):
		return flask.render_template('tanzimprofile.html')
	@login_required
	def post(self):
		if 'reset' in flask.request.form:
			return flask.redirect(flask.url_for('tanzimprofile'))
		
		user=flask.session['username']

		#be nazaram oon jayi ke dare signup mishe bayad node profile khali sakhte she inja propertie hash por she .
		if 'send' in flask.request.form:

			q = """start n=node(*) return n"""
			lookup = Q("Id", exact=str(user))
			results = gdbpro.nodes.filter(lookup) 
			
			#a = [flask.request.form['firstname'],flask.request.form['lastname'],flask.request.form['mail'],flask.request.form['age'],flask.request.form['country'],flask.request.form['biography'],flask.request.form['education'],flask.request.form['work'],flask.request.form['college'],flask.request.form['school']]
			#for i in range(len(a)):
			#	if (a[i] == ""):
			#		a[i]="-"
			n = gdbpro.node[results[0].id]
			n['firstname']=flask.request.form['firstname']
			n['lastname']=flask.request.form['lastname']
			n['mail']=flask.request.form['mail']
			n['age']=flask.request.form['age']
			n['country']=flask.request.form['country']
			n['biography']=flask.request.form['biography']
			#n['gender']=flask.request.form['male']
			n['education']=flask.request.form['education']
			n['work']=flask.request.form['work']
			n['college']=flask.request.form['college']
			n['school']=flask.request.form['school']
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

		if 'send' in flask.request.form:

			if (y!="" and m!="" and da!=""):
				d=gdbd.nodes.create(diarie=flask.request.form['table'])
				diaries.add(d)
				q = """start n=node(*) return n"""
				lookup = Q("username", exact=str(user))
				results = gdbp.nodes.filter(lookup) 

				for i in range(len(results)):
					n = gdbp.node[results[i].id]
					n.relationships.create("wrote",d,year=y,month=m,day=da)
		
				return flask.redirect(flask.url_for('test'))
		
			else:
				flask.flash("you must write date!")
				print("you must write date!")
				return flask.redirect(flask.url_for('writing'))

		if 'log out' in flask.request.form:
			flask.session.pop('username',None)
			return flask.redirect(flask.url_for('main'))
	


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

app.add_url_rule('/signin/home/friendprofile/',
                 view_func =  friendprofile.as_view('friendprofile'),
                 methods = ['GET','POST'])


app.add_url_rule('/signin/home/profile/tanzimprofile/',
                 view_func =  tanzimprofile.as_view('tanzimprofile'),
                 methods = ['GET','POST'])

app.debug = True
app.run()











