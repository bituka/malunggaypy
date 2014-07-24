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

class AdminPage(webapp2.RequestHandler):
  def get(self):       
        
    user = users.get_current_user()
    if (user and user.nickname() == 'goryo.webdev'):

    #  mainentries = db.GqlQuery("SELECT * FROM MainEntries")
      
      template_values = {
    #    'mainentries': mainentries,
      }
      
      template = jinja_environment.get_template('admin.html')
      self.response.out.write(template.render(template_values))
    else:
        
      self.redirect(users.create_login_url(self.request.uri))

        
  def post(self):   
    portfolio = Portfolio()
    portfolio.title = self.request.get('title')   
    portfolio.description = self.request.get('description')
    portfolio.link_url = self.request.get('link_url')
    image = self.request.get('img')
    portfolio.image = db.Blob(image)
    portfolio.put()
    self.redirect('/admin')

app = webapp2.WSGIApplication([('/', MainPage),
                                ('/admin', AdminPage),
                                ],
                                debug=True)
                              
                              
