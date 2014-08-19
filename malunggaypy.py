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
  titulo = db.StringProperty(required=True, default="wala")
  kategorya = db.StringProperty(required=True, default="wala") #pelikula, teleserye, palabas
  letrato_link = db.StringProperty(required=True, default="wala")
#  uri = db.StringProperty(required=True)
  date_created = db.DateTimeProperty(auto_now_add=True, default="wala")
  date_updated = db.DateProperty()

# controllers
# TODO display entries to public folder
class MainPage(webapp2.RequestHandler):
  def get(self):
    
    mainentries = db.GqlQuery("SELECT * FROM MainEntries")

    template_values = {
      'mainentries': mainentries,
    }

    template = jinja_environment.get_template('index.html')
    self.response.out.write(template.render(template_values))

class AdminPage(webapp2.RequestHandler):
  def get(self):
        
    '''
    user = users.get_current_user()
    if (user and user.nickname() == 'goryo.webdev'):

    #  mainentries = db.GqlQuery("SELECT * FROM MainEntries")
      
      template_values = {
    #    'mainentries': mainentries,
      }
    '''
    mainentries = db.GqlQuery("SELECT * FROM MainEntries")
    
    template_values = {
      'mainentries': mainentries,
    }

    template = jinja_environment.get_template('admin.html')
    self.response.out.write(template.render(template_values))
    

    '''
    else:
        
      self.redirect(users.create_login_url(self.request.uri))
    '''
        
  def post(self):
    
    mainentries = MainEntries()
    mainentries.titulo = self.request.get('titulo')
    mainentries.kategorya = self.request.get('kategorya')
    mainentries.letrato_link = self.request.get('letrato_link')

    mainentries.put()
    self.redirect('/admin')


class EditDeleteEntriesPage(webapp2.RequestHandler):
  def get(self):
        
    '''
    user = users.get_current_user()
    if (user and user.nickname() == 'goryo.webdev'):

    #  mainentries = db.GqlQuery("SELECT * FROM MainEntries")
      
      template_values = {
    #    'mainentries': mainentries,
      }
    '''
    mainentries = db.GqlQuery("SELECT * FROM MainEntries")
    
    template_values = {
      'mainentries': mainentries,
    }

    template = jinja_environment.get_template('editdeleteentries.html')
    self.response.out.write(template.render(template_values))
    
    
    '''
    else:
        
      self.redirect(users.create_login_url(self.request.uri))
    '''
        
  def post(self):
    mainentries = MainEntries()
    mainentries.titulo = self.request.get('titulo')
    mainentries.kategorya = self.request.get('kategorya')
    mainentries.letrato_link = self.request.get('letrato_link')

    mainentries.put()
    self.redirect('/admin')


class EditSingleEntry(webapp2.RequestHandler):
  def get(self):
    
    mainentry = db.get(self.request.get('id'))

    template_values = {
      'mainentry' : mainentry
    }

    template = jinja_environment.get_template('editsingleentry.html')
    self.response.out.write(template.render(template_values))
    

  def post(self):
    mainentries = db.get(self.request.get('id'))
    mainentries.titulo = self.request.get('titulo')
    mainentries.kategorya = self.request.get('kategorya')
    mainentries.letrato_link = self.request.get('letrato_link')
    mainentries.put()
    self.redirect('/editdeleteentries')


class DeleteMainEntry(webapp2.RequestHandler):
  def post(self):
    mainentry = db.get(self.request.get('id'))
    mainentry.delete()
    self.redirect('/editdeleteentries')


#For viewing single entry - this is public
class ViewSingleEntry(webapp2.RequestHandler):
  def get(self):
    
    mainentry = db.get(self.request.get('id'))

    template_values = {
      'mainentry' : mainentry
    }

    template = jinja_environment.get_template('viewsingleentry.html')
    self.response.out.write(template.render(template_values))

app = webapp2.WSGIApplication([('/', MainPage),
                                ('/admin', AdminPage),
                                ('/editdeleteentries', EditDeleteEntriesPage),
                                ('/editsingleentry', EditSingleEntry),
                                ('/deletemainentry', DeleteMainEntry),
                                ('/viewsingleentry', ViewSingleEntry),
                                ],
                                debug=True)
                              
                              
