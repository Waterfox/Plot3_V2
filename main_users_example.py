#Plot3v2 main program
# +++++++++++++++++++++++++++++++++++++++++++WFDN+++++++++++++++++++++++++++++++++++
import webapp2
import jinja2, os, logging, cgi ,json, random, time
from google.appengine.ext import db
from google.appengine.api import memcache, mail, users
from webfunctions import validate_name, validate_pass, validate_match, validate_email, make_salt, make_pw_hash, valid_pw, make_secure_val, check_secure_val, validate_cats, validate_title
from colors import *
jinja_environment = jinja2.Environment(autoescape=False,loader=jinja2.FileSystemLoader(os.path.join(os.path.dirname(__file__),'templates2')))


B = """
<input type="button" class="button"  value="Bar Plot" onmouseup="window.location = '%(id)s?ptype=bar'" >
"""
BP = """
<input type="button" class="button"  value="Bar Plot" onmouseup="window.location = '%(id)s?ptype=bar'" >
<input type="button" class="button"  value="Pie Plot" onmouseup="window.location = '%(id)s?ptype=pie'" >
"""
LASB = """
<input type="button" class="button"  value="Line Plot" onmouseup="window.location = '%(id)s?ptype=line'" >
<input type="button" class="button"  value="Area Plot" onmouseup="window.location = '%(id)s?ptype=area'" >
<input type="button" class="button"  value="Scatter Plot" onmouseup="window.location = '%(id)s?ptype=scatter'" >
<input type="button" class="button"  value="Bar Plot" onmouseup="window.location = '%(id)s?ptype=bar'" >
"""

FOOTER = """
<footer>
	Powererd by  <a href="https://github.com/mbostock/d3/wiki">D3</a> and <a href="http://nvd3.com/">NVD3</a>.
</footer>
"""

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


class DSET(db.Model,Plot3Handler):
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

class PLOT(db.Model,Plot3Handler):
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
		self.redirect(URL)
		#cSet = 'Rset3'
		#self.render('Landing.html',colorset=colorDict[cSet])

class HomeBaseHandler(Plot3Handler):
	def get(self):
		[loggedIn,UN] = self.checkUser()
		URL = users.create_logout_url(dest_url="/")
		self.response.out.write("<a href = %s>logout</a>" %URL)
		#if loggedIn:
		#	self.render('HomeBase.html')


app = webapp2.WSGIApplication([	('/', MainHandler),
								('/homeBase',HomeBaseHandler),
								('/landing',LandingHandler)],
                  debug=True)