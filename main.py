import webapp2
import os
import datetime
import json
import urllib

#Custom imports
import datamodel

#Imports from Google Library
from google.appengine.ext import db
from google.appengine.ext import blobstore
from google.appengine.ext.webapp import blobstore_handlers
from google.appengine.ext.webapp import template
from google.appengine.api import users

path = os.path.join(os.path.dirname(__file__), 'index.html')
admin_template = os.path.join(os.path.dirname(__file__), 'admin.html')

class MainHandler(webapp2.RequestHandler):
  def get(self):
    # stores=[]
    offers = db.GqlQuery("SELECT * FROM Offers")
    stores = db.GqlQuery("SELECT * FROM Stores")
    today = datetime.date.today()
    # stores.append(db_stores)
    offers_list = []
    for offer in offers:
      offers_list.append(datetime.datetime.now() - offer.posted_on)
      # offers[offers.key].
    
    template_values = {
      'name': "Mahesh",'offers':offers,'stores':stores,'today':today,'offers_list':offers_list
    }
    self.response.out.write(template.render(path, template_values))

class Signin(webapp2.RequestHandler):
    def get(self):
        user = users.get_current_user()
        if user:
            
            greeting = ('Welcome, %s! (<a href="%s">sign out</a>)' %
                        (user.nickname(), users.create_logout_url('/')))
        else:
            greeting = ('<a href="%s">Sign in or register</a>.' %
                        users.create_login_url('/'))

        self.response.out.write('<html><body>%s</body></html>' % greeting)

class PhotoUploadHandler(blobstore_handlers.BlobstoreUploadHandler):
    def get(self):
      upload_url = blobstore.create_upload_url('/upload_photo')
      # self.response.write('<form method="post" action="'+upload_url+'"><input type="file"/><input type="submit" /></form>')
      self.response.out.write('<html><body>')
      self.response.out.write('<form action="%s" method="POST" enctype="multipart/form-data">' % upload_url)
      self.response.out.write("""Upload File: <input type="file" name="file"><br> <input type="submit"
      name="submit" value="Submit"> </form></body></html>""")

      
    def post(self):
        try:
            upload = self.get_uploads()[0]
            t=upload.key()
            self.response.out.headers["Content-Type"]="application/json"
            output={'blob_key':str(t)}
            output=json.dumps(output)
            self.response.out.write(output)
            # self.redirect('/view_photo/%s' % upload.key())


        except Exception as exc:
            # self.redirect('/upload_failure.html')
            self.response.write("Exception")
            self.response.write(exc)

class PhotoServeHandler(blobstore_handlers.BlobstoreDownloadHandler):
  def get(self, resource):
    if not blobstore.get(resource):
            self.error(404)
    else:
            resource = str(urllib.unquote(resource))
            blob_info = blobstore.BlobInfo.get(resource)
            self.send_blob(blob_info)
    
class ViewPhotoHandler(blobstore_handlers.BlobstoreDownloadHandler):
    def get(self, photo_key):
        if not blobstore.get(photo_key):
            self.error(404)
        else:
            self.send_blob(photo_key)
            
class OfferPage(webapp2.RequestHandler):
    def get(self):
        key=self.request.get('key')
        offer=db.GqlQuery("SELECT * FROM Offers where key = :1",key)
        self.response.write(offer)

app = webapp2.WSGIApplication([
  ('/', MainHandler),('/offer',OfferPage),('/signin',Signin),('/upload_photo', PhotoUploadHandler),('/view_photo/([^/]+)?',PhotoServeHandler)
], debug=True)