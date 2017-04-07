#Bulid a blog exercise for LC101, the first project to utilize a database

import webapp2
import jinja2
import os

from google.appengine.ext import db

# set up jinja2
template_dir = os.path.join(os.path.dirname(__file__), "templates")
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir), autoescape=True)

class MainHandler(webapp2.RequestHandler):
    def get(self):

        t = jinja_env.get_template("front-page.html")
        content = t.render()
        self.response.write(content)

app = webapp2.WSGIApplication([
    ('/', MainHandler)
], debug=True)
