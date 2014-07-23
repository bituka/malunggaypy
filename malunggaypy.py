import webapp2
import jinja2
import os
import cgi
import datetime
import urllib
import sys

from google.appengine.ext import db
from google.appengine.api import images
from google.appengine.api import users

jinja_environment = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)))

#models
class MainEntries(db.Model):
  titulo = db.StringProperty(required=True)
  kategorya = db.StringProperty(required=True) #pelikula, teleserye, palabas
  letrato_link = db.StringProperty(required=True)
#  uri = db.StringProperty(required=True) 
  date_created = db.DateTimeProperty(auto_now_add=True)
  date_updated = db.DateProperty()

# controllers
class MainPage(webapp2.RequestHandler):
  def get(self):       
    
    template_values = {
      
    }

    template = jinja_environment.get_template('index.html')
    self.response.out.write(template.render(template_values))
            
        
app = webapp2.WSGIApplication([('/', MainPage),
                                ],
                                debug=True)
                              
                              
