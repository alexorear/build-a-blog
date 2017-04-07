#Bulid a blog exercise for LC101, the first project to utilize a database

import webapp2
import jinja2
import os

from google.appengine.ext import db

# set up jinja2
template_dir = os.path.join(os.path.dirname(__file__), "templates")
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir), autoescape=True)

class MainHandler(webapp2.RequestHandler):
    def front_page(self, title = "", body = "", error = ""):

        t = jinja_env.get_template("front-page.html")
        content = t.render(title = title, body = body, error = error)
        self.response.write(content)

    def get(self):

        self.front_page()

    def post(self):
        title = self.request.get("title")
        body = self.request.get("body")

        if title and body:
            self.response.write("Thanks!")
        else:
            error = "Please enter a title and some body text"
            self.front_page(title, body, error)


app = webapp2.WSGIApplication([
    ('/', MainHandler)
], debug=True)
