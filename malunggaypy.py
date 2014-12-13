import webapp2
import jinja2
import os
import cgi
import datetime
import urllib
import sys, traceback
import json
import tzsearch
import libs.paging

from libs.paging import *
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
  date_created = db.DateTimeProperty(auto_now_add=True, default="wala")
  date_updated = db.DateProperty()

'''
class MainEntries(tzsearch.SearchableModel):
  titulo = db.StringProperty(required=True, default="wala")
  kategorya = db.StringProperty(required=True, default="wala") #pelikula, teleserye, palabas
  letrato_link = db.StringProperty(required=True, default="wala")
  date_created = db.DateTimeProperty(auto_now_add=True, default="wala")
  date_updated = db.DateProperty()
'''

# controllers
# TODO display entries to public folder
class MainPage(webapp2.RequestHandler):
  def get(self):
    
    mainentries = db.GqlQuery("SELECT titulo, letrato_link FROM MainEntries ORDER BY date_created DESC LIMIT 30")

    template_values = {
      'mainentries': mainentries,


    }

    template = jinja_environment.get_template('index.html')
    self.response.out.write(template.render(template_values))

class AdminPage(webapp2.RequestHandler):
  def get(self):
        
    user = users.get_current_user()
    
    if (user and user.nickname() == 'goryo.webdev'):
    
      mainentries = db.GqlQuery("SELECT titulo, letrato_link, kategorya FROM MainEntries")

      template_values = {
        'mainentries': mainentries,
      }

      template = jinja_environment.get_template('admin.html')
      self.response.out.write(template.render(template_values))
    
    else:
        
      self.redirect(users.create_login_url(self.request.uri))
    
        
  def post(self):
    
    mainentries = MainEntries()
    mainentries.titulo = self.request.get('titulo')
    mainentries.kategorya = self.request.get('kategorya')
    mainentries.letrato_link = self.request.get('letrato_link')

    mainentries.put()
    self.redirect('/admin')


class EditDeleteEntriesPage(webapp2.RequestHandler):
  def get(self):
        
    user = users.get_current_user()
    
    if (user and user.nickname() == 'goryo.webdev'):

      mainentries = db.GqlQuery("SELECT * FROM MainEntries")

      template_values = {
        'mainentries': mainentries,
      }

      template = jinja_environment.get_template('editdeleteentries.html')
      self.response.out.write(template.render(template_values))
    
    
    else:
        
      self.redirect(users.create_login_url(self.request.uri))
    
        
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


class SearchEntries(webapp2.RequestHandler):

    def post(self):

      whatever = self.request.get('term')

      results = MainEntries.all().search(whatever).fetch(20)

      '''
      # Testing results
      if results is not None:
        for resulta in results:
          self.response.out.write(resulta.titulo)
          self.response.out.write(whatever)
      else:
        print('results is None')
      '''

      template_values = {
      'results' : results
      }

      template = jinja_environment.get_template('search.html')
      self.response.out.write(template.render(template_values))


class BrowsePage(webapp2.RequestHandler):

    def get(self):


      template_values = {
       
      }

      template = jinja_environment.get_template('browse.html')
      self.response.out.write(template.render(template_values))
      
      
class BrowsePagePelikula(webapp2.RequestHandler):

    def get(self):

      '''
      titulo = db.StringProperty(required=True, default="wala")
      kategorya = db.StringProperty(required=True, default="wala") #pelikula, teleserye, palabas
      letrato_link = db.StringProperty(required=True, default="wala")
      date_created = db.DateTimeProperty(auto_now_add=True, default="wala")
      date_updated = db.DateProperty()
      '''

      #TODO 
      nextqueryhascontents = False
      

      query = db.GqlQuery("SELECT titulo, letrato_link FROM MainEntries WHERE kategorya = 'pelikula' ORDER BY date_created DESC")
      
      cursor = self.request.get('cursor')
      if cursor: 
        query.with_cursor(start_cursor=cursor)
      
      mainentries = query.fetch(30)
      cursor = query.cursor()
      
      # check if next query has contents
      query.with_cursor(start_cursor=cursor)
      main_e = query.fetch(1)

      if main_e:
        nextqueryhascontents = True
      else:
        nextqueryhascontents = False


      template_values = {
      
       'cursor': cursor,
       'mainentries': mainentries,
       'nextqueryhascontents' : nextqueryhascontents
      
      }


      template = jinja_environment.get_template('browsepelikula.html')
      self.response.out.write(template.render(template_values))



class BrowsePageSeries(webapp2.RequestHandler):

    def get(self):

      query = db.GqlQuery("SELECT titulo, letrato_link FROM MainEntries WHERE kategorya = 'series' ORDER BY date_created DESC")
      
      cursor = self.request.get('cursor')
      if cursor: query.with_cursor(start_cursor=cursor)
      mainentries = query.fetch(30)
      cursor = query.cursor()
      
      # check if next query has contents
      query.with_cursor(start_cursor=cursor)
      main_e = query.fetch(1)

      if main_e:
        nextqueryhascontents = True
      else:
        nextqueryhascontents = False


      template_values = {
      
       'cursor': cursor,
       'mainentries': mainentries,
       'nextqueryhascontents' : nextqueryhascontents
      
      }


      template = jinja_environment.get_template('browseseries.html')
      self.response.out.write(template.render(template_values))

class BrowsePagePalabas(webapp2.RequestHandler):

    def get(self):

      
      query = db.GqlQuery("SELECT titulo, letrato_link FROM MainEntries WHERE kategorya = 'palabas' ORDER BY date_created DESC")
      cursor = self.request.get('cursor')
      if cursor: query.with_cursor(start_cursor=cursor)
      mainentries = query.fetch(30)
      cursor = query.cursor()
      
      # check if next query has contents
      query.with_cursor(start_cursor=cursor)
      main_e = query.fetch(1)

      if main_e:
        nextqueryhascontents = True
      else:
        nextqueryhascontents = False

      template_values = {
      
       'cursor': cursor,
       'mainentries': mainentries,
       'nextqueryhascontents' : nextqueryhascontents
      }


      template = jinja_environment.get_template('browsepalabas.html')
      self.response.out.write(template.render(template_values))


class BrowsePageTeleserye(webapp2.RequestHandler):

    def get(self):

      
      query = db.GqlQuery("SELECT titulo, letrato_link FROM MainEntries WHERE kategorya = 'teleserye' ORDER BY date_created DESC")
      cursor = self.request.get('cursor')
      if cursor: query.with_cursor(start_cursor=cursor)
      mainentries = query.fetch(30)
      cursor = query.cursor()
      
      # check if next query has contents
      query.with_cursor(start_cursor=cursor)
      main_e = query.fetch(1)

      if main_e:
        nextqueryhascontents = True
      else:
        nextqueryhascontents = False


      template_values = {
      
       'cursor': cursor,
       'mainentries': mainentries,
       'nextqueryhascontents' : nextqueryhascontents
      
      }

      template = jinja_environment.get_template('browseteleserye.html')
      self.response.out.write(template.render(template_values))


class BrowsePagePinoyIndie(webapp2.RequestHandler):

    def get(self):
      
      query = db.GqlQuery("SELECT titulo, letrato_link FROM MainEntries WHERE kategorya = 'pinoyindie' ORDER BY date_created DESC")
      cursor = self.request.get('cursor')
      if cursor: query.with_cursor(start_cursor=cursor)
      mainentries = query.fetch(30)
      cursor = query.cursor()
      
      # check if next query has contents
      query.with_cursor(start_cursor=cursor)
      main_e = query.fetch(1)

      if main_e:
        nextqueryhascontents = True
      else:
        nextqueryhascontents = False

      template_values = {
      
       'cursor': cursor,
       'mainentries': mainentries,
       'nextqueryhascontents' : nextqueryhascontents
      
      }


      template = jinja_environment.get_template('browsepinoyindie.html')
      self.response.out.write(template.render(template_values))


class BrowsePageKoreanobela(webapp2.RequestHandler):

    def get(self):

      query = db.GqlQuery("SELECT titulo, letrato_link FROM MainEntries WHERE kategorya = 'koreanobela' ORDER BY date_created DESC")
      cursor = self.request.get('cursor')
      if cursor: query.with_cursor(start_cursor=cursor)
      mainentries = query.fetch(30)
      cursor = query.cursor()


      # check if next query has contents
      query.with_cursor(start_cursor=cursor)
      main_e = query.fetch(1)

      if main_e:
        nextqueryhascontents = True
      else:
        nextqueryhascontents = False
      

      template_values = {
      
       'cursor': cursor,
       'mainentries': mainentries,
       'nextqueryhascontents' : nextqueryhascontents
      }


      template = jinja_environment.get_template('browsekoreanobela.html')
      self.response.out.write(template.render(template_values))


app = webapp2.WSGIApplication([('/', MainPage),
                                ('/admin', AdminPage),
                                ('/editdeleteentries', EditDeleteEntriesPage),
                                ('/editsingleentry', EditSingleEntry),
                                ('/deletemainentry', DeleteMainEntry),
                                ('/viewsingleentry', ViewSingleEntry),
                                ('/searchentries', SearchEntries),
                                ('/browse', BrowsePage),
                                ('/pelikula', BrowsePagePelikula),
                                ('/palabas', BrowsePagePalabas),
                                ('/teleserye', BrowsePageTeleserye),
                                ('/pinoyindie', BrowsePagePinoyIndie),
                                ('/series', BrowsePageSeries),
                                ('/koreanobela', BrowsePageKoreanobela)
                                ],
                                debug=True)
                              
                              
