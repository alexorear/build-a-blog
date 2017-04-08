#Bulid a blog exercise for LC101, the first project to utilize a database

import webapp2
import jinja2
import os

from google.appengine.ext import db

# set up jinja2
template_dir = os.path.join(os.path.dirname(__file__), "templates")
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir), autoescape=True)

class Post(db.Model):
    title = db.StringProperty(required = True)
    body = db.TextProperty(required = True)
    created = db.DateTimeProperty(auto_now_add = True)

class MakePostHandler(webapp2.RequestHandler):
    def front_page(self, title = "", body = "", error = ""):

        t = jinja_env.get_template("/newpost.html")
        content = t.render(title = title, body = body, error = error)
        self.response.write(content)

    def get(self):

        self.front_page()

    def post(self):
        title = self.request.get("title")
        body = self.request.get("body")

        if title and body:
            a = blog_post(title = title, body = body)
            self.redirect("/blog")
        else:
            error = "Please enter a title and some body text"
            self.front_page(title, body, error)


class BlogHandler(webapp2.RequestHandler):
    def get(self):

        self.response.write("There will be a blog here soon.")

app = webapp2.WSGIApplication([
    ('/newpost', MakePostHandler),
    ('/blog', BlogHandler)
], debug=True)
