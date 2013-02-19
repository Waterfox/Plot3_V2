#Plot3v2 main program
# +++++++++++++++++++++++++++++++++++++++++++WFDN+++++++++++++++++++++++++++++++++++
import webapp2
import jinja2, os, logging, cgi ,json, random, time
from google.appengine.ext import db
from google.appengine.api import memcache, mail, users
from webfunctions import validate_name, validate_pass, validate_match, validate_email, make_salt, make_pw_hash, valid_pw, make_secure_val, check_secure_val, validate_cats, validate_title
from colors import *
jinja_environment = jinja2.Environment(autoescape=False,loader=jinja2.FileSystemLoader(os.path.join(os.path.dirname(__file__),'templates2')))


class Plot3Handler(webapp2.RequestHandler):
	def render_str(self, template, **params):
		t=jinja_environment.get_template(template)
		return t.render(params)	

	def render(self, template, **kw):
		self.response.out.write(self.render_str(template,**kw))	

	def checkUser(self):
		user=users.get_current_user()
		if user:
			return True,user.user_id()
		else:
			return False,'0'
		
	def checkCookies(self):
		UNH = self.request.cookies.get('UNH','0')
		
		if check_secure_val(UNH):
			id = UNH.split('|')[0]
			q = UNPW.get_by_id(int(id))
			UN = q.UN
			loggedIn = True
		else:
			loggedIn = False
			UN = '0'
		
		return loggedIn,UN


class DSET(db.Model,Plot3Handler): #Datastore for user's datasets
	UN = db.StringProperty(required = True) #userID
	TS = db.DateTimeProperty(auto_now_add = True) #timestamp
	CATS = db.ListProperty(str) #categories
	PLOTDATA = db.TextProperty(required = True) #json data block
	TITLE = db.StringProperty(required = True) #data set ID
	DESC = db.TextProperty()	#description
	XL = db.StringProperty()	#y-axis Label
	YL = db.StringProperty()	#x-axis Label
	SZ = db.StringProperty()	#number of datapoints in the set
	TYPE = db.StringProperty() # type of data, see documentation for available types
	ACCESS = db.ListProperty(str,required = True)

class PLOT(db.Model,Plot3Handler): #Datastore for user's plots
	UN = db.StringProperty(required = True) #userID
	TS = db.DateTimeProperty(auto_now_add = True) #timestamp
	CATS = db.ListProperty(str) #categories
	SETS = db.ListProperty(str) #data sets contained in plot
	DESC = db.TextProperty()	#description
	XL = db.StringProperty()	#y-axis Label
	YL = db.StringProperty()	#x-axis Label
	XF = db.StringProperty()	#x-axis format
	YF = db.StringProperty()	#y-axis format
	TYPE = db.StringProperty(required = True) # type of plot, see documentation for available types
	ACCESS = db.ListProperty(str,required = True)

class DASH(db.Model,Plot3Handler):	#Datastore for user's dashboards
	UN = db.StringProperty(required = True) #userID
	TS = db.DateTimeProperty(auto_now_add = True) #timestamp
	CATS = db.ListProperty(str) #categories
	DASHDATA = db.TextProperty(required = True) #json data block
	TITLE = db.StringProperty(required = True) #data set ID
	DESC = db.TextProperty()	#description
	ACCESS = db.ListProperty(str,required = True)

class UNPW(db.Model):
	UN = db.StringProperty(required = True) #userID
	EM = db.EmailProperty()		#email in case users is out of date
	TS = db.DateTimeProperty(auto_now_add = True)	#time
	CSET = db.StringProperty()		#default colour set
	STATUS = db.StringProperty()	#admin
	DASH = db.ListProperty(str)		#List of dashboard objects
	CLIST = db.ListProperty(db.Text)
	
class COMMENTS(db.Model):
	UN = db.StringProperty() #username
	COMM = db.TextProperty(required = True)
	TS = db.DateTimeProperty(auto_now_add=True)
	EM = db.EmailProperty()



class MainHandler(Plot3Handler):
    def get(self):
	
		#Get and check the cookie, find the UN
		[loggedIn,UN] = self.checkUser()

		if loggedIn is False:
			self.redirect('/landing')
			return
		else:
			self.redirect('/homeBase')


class LandingHandler(Plot3Handler):
	def get(self):
		URL=users.create_login_url("/")
		self.response.out.write("<a href = %s>login</a>" %URL)
		cSet = 'Rset3'
		self.render('Landing.html',colorset=colorDict[cSet])

class HomeBaseHandler(Plot3Handler):
	def get(self):
		[loggedIn,UN] = self.checkUser()
		if loggedIn:
			URL = users.create_logout_url(dest_url="/")
			self.response.out.write("<a href = %s>logout</a>" %URL)
			self.render('HomeBase.html')


class PlotDisplay(Plot3Handler):
	def get(self):
		[loggedIn,UN] = self.checkUser()
		return

class PlotOrganizer(Plot3Handler):
	def get(self):
		[loggedIn,UN] = self.checkUser()
		return

class PlotBuilder(Plot3Handler):
	def get(self):
		[loggedIn,UN] = self.checkUser()
		return

class PlotLiveDisplay(Plot3Handler):
	def get(self):
		[loggedIn,UN] = self.checkUser()
		return

class PlotLiveOrganizer(Plot3Handler):
	def get(self):
		[loggedIn,UN] = self.checkUser()
		return

class PlotLiveBuilder(Plot3Handler):
	def get(self):
		[loggedIn,UN] = self.checkUser()
		return

class DataBuilder(Plot3Handler):
	def get(self):
		[loggedIn,UN] = self.checkUser()
		return

class DataOrganizer(Plot3Handler):
	def get(self):
		[loggedIn,UN] = self.checkUser()
		return

class DataLiveBuilder(Plot3Handler):
	def get(self):
		[loggedIn,UN] = self.checkUser()
		return

class DataLiveOrganizer(Plot3Handler):
	def get(self):
		[loggedIn,UN] = self.checkUser()
		return

class DashboardDisplay(Plot3Handler):
	def get(self):
		[loggedIn,UN] = self.checkUser()
		return

class DashboardOrganizer(Plot3Handler):
	def get(self):
		[loggedIn,UN] = self.checkUser()
		return

class DashboardBuilder(Plot3Handler):
	def get(self):
		[loggedIn,UN] = self.checkUser()
		return


APPURLS = 		[	('/', MainHandler),
				('/HomeBase',HomeBaseHandler),
				('/Landing',LandingHandler),
				('/Contact',ContactHandler),
				('/Plot([0-9]+)'PlotDisplay),
				('/PlotOrganizer'PlotBuilder),
				('/PlotBuilder'PlotBuilder),
				('/PlotLive([0-9]+)'PlotDisplay),
				('/PlotLiveOrganizer'PlotLiveOrganizer),
				('/PlotLiveBuilder'PlotLiveBuilder),
				('/DataBuilder'DataBuilder),
				('/DataOrganizer'DataOrganizer),
				('/DataLiveBuilder'DataBuilder),
				('/DataLiveOrganizer'DataOrganizer),
				('/Dashboard([0-9]+)'DashboardDisplay),
				('/DashboardOrganizer'DashboardOraganizer),
				('/DashboardBuilder'DashboardBuilder)
				]


app = webapp2.WSGIApplication(APPURLS,debug=True)