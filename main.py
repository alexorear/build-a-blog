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
            a = Post(title = title, body = body)
            a.put()
            self.redirect("/blog")
        else:
            error = "Please enter a title and some body text"
            self.front_page(title, body, error)


class BlogHandler(webapp2.RequestHandler):
    def get(self):
        posts = db.GqlQuery("SELECT * FROM Post ORDER BY created DESC LIMIT 5")

        t = jinja_env.get_template("/blog.html")
        content = t.render(posts = posts)
        self.response.write(content)

class ViewPostHandler(webapp2.RequestHandler):
        def get(self, id):
            id = int(id)
            post = Post.get_by_id(id)

            t = jinja_env.get_template("/blog_post.html")
            content = t.render(post = post)
            self.response.write(content)


app = webapp2.WSGIApplication([
    ('/newpost', MakePostHandler),
    ('/blog', BlogHandler),
    webapp2.Route('/blog/<id:\d+>', ViewPostHandler)
], debug=True)
