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
            # user_photo = UserPhoto(user=users.get_current_user().user_id(),
                                  # blob_key=upload.key())
            # db.put(user_photo)
            
            # self.redirect('/view_photo/%s' % upload.key())
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

class Admin(webapp2.RequestHandler):
      def get(self):
        user = users.get_current_user()
        upload_url = blobstore.create_upload_url('/upload_photo')
        try:
            if user:
                # self.response.write("User is present")
                my_user = db.GqlQuery("SELECT * FROM Users WHERE email = :1",user.email())
                my_user = my_user.fetch(1)
                if len(my_user)==1:
                    for e in my_user:
                        # self.response.write("str(e.user_type()")
                        if e.user_type=="Admin":
                            template_values = {
                              'name': "World","upload_url":upload_url
                            }
                            self.response.out.write(template.render(admin_template, template_values))
                        else:
                            self.redirect("/")
                if len(my_user)==0:
                    new_user=datamodel.Users(user=user,user_type="Regular",name=user.nickname(),email=user.email())
                    new_user.put()
            else:
                self.redirect(users.create_login_url('/'))
        except Exception as exc:
            self.response.write(exc)

      def post(self):
        user = users.get_current_user()
        try:
            if user:
                my_user = db.GqlQuery("SELECT * FROM Users WHERE email = :1",user.email())
                my_user = my_user.fetch(1)
                if len(my_user)==1:
                    for e in my_user:
                        if e.user_type=="Admin":
                          database =self.request.get("database")
                          if database=="offer":
                            store        =   self.request.get('store')
                            title        =   self.request.get('title')
                            offer_position=  self.request.get('offer_kind')
                            offer_type   =   self.request.get('offer_type')
                            coupon_code  =   self.request.get('coupon_code')
                            aff_link     =   self.request.get('store_aff_link')
                            description  =   self.request.get('description')
                            expiry       =   self.request.get('expiry')
                            posted_on    =   self.request.get('posted_on')
                            category     =   self.request.get('category')
                            sub_category =   self.request.get('sub_category')
                            ideal_for    =   self.request.get('ideal_for')
                            blob_key     =   self.request.get('blob_key')  
                            expiry       =   datetime.datetime.strptime(expiry, '%d/%m/%Y').date()
                            editors_pick =   bool(self.request.get("editors_pick"))
                            enabled      =   bool(self.request.get("enabled"))

                            offer        =   datamodel.Offers(store=store,title=title,offer_position=offer_position,
                                             offer_type=offer_type,coupon_code=coupon_code,aff_link=aff_link,
                                             description=description,expiry=expiry,category=category,sub_category=sub_category,
                                             ideal_for=ideal_for,enabled=enabled,editors_pick=editors_pick)
                            if blob_key!="":
                                offer.blob_key=blob_key
                            offer.put()
                            self.response.write("Offer Successfully Submitted")
                            
                          else:
                            store_name        =   self.request.get('store')
                            affid        =   self.request.get('affid')
                            tag_name     =   self.request.get('tag_name')
                            store_link     =   self.request.get("store_aff_link")
                            store        =   datamodel.Stores(store=store_name, affid=affid,tagname=tag_name, store_link = store_link)
                            blob_key     =   self.request.get('blob_key')  
                            if blob_key!="":
                                store.blob_key=blob_key
                            store.put()
                            self.response.write("Store is successfully submitted")
                            
                        else:
                            self.redirect("/")
                if len(my_user)==0:
                    new_user=datamodel.Users(user=user,user_type="Regular",name=user.nickname(),email=user.email())
                    new_user.put()
            else:
                self.redirect(users.create_login_url('/'))
        except Exception as exc:
            self.response.write(exc)

app = webapp2.WSGIApplication([
  ('/', MainHandler),('/signin',Signin),('/upload_photo', PhotoUploadHandler),('/admin',Admin),('/view_photo/([^/]+)?',PhotoServeHandler)
], debug=True)