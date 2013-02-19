# Plot3v2 database classes
from google.appengine.ext import db


class DSET(db.Model,Plot3Handler):
	UN = db.StringProperty(required = True) #username
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
	UN = db.StringProperty(required = True) #username #username
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
	UN = db.StringProperty(required = True) #username #username
	EM = db.EmailProperty()		#email in case users is out of date
	TS = db.DateTimeProperty(auto_now_add = True)	#time
	CSET = db.StringProperty()		#default colour set
	STATUS = db.StringProperty()	#admin
	DASH = db.ListProperty(str)		#List of dashboard objects
	
class COMMENTS(db.Model):
	UN = db.StringProperty() #username
	COMM = db.TextProperty(required = True)
	TS = db.DateTimeProperty(auto_now_add=True)
	EM = db.EmailProperty()
