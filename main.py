                                                                                                                                                                                                                                                         #Bulid a blog exercise for LC101, the first project to utilize a database

import webapp2
import jinja2
import os

from google.appengine.ext import db

# set up jinja2
template_dir = os.path.join(os.path.dirname(__file__), "templates")
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir), autoescape=True)

def get_posts(limit, offset):
    """returns a set number of post offset by user defined number"""
    posts = db.GqlQuery("SELECT * FROM Post ORDER BY created DESC LIMIT {0} OFFSET {1}" .format(limit, offset))
    return posts

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
            id = str(a.key().id())
            self.redirect("/blog/" + id)
        else:
            error = "Please enter a title and some body text"
            self.front_page(title, body, error)


class BlogHandler(webapp2.RequestHandler):
    def get(self):
        #Count total number of blog post
        posts = db.GqlQuery("SELECT * FROM Post")
        total_posts = posts.count()
        #Get current blog page
        page = self.request.get("page")
        #Gql Query limit
        limit = 4
        #Empty variables for previous/next page params for template
        nxt = ""
        prv = ""

        #Check blog page to see if template should display next or previous links
        if page and page != "0" and page != "1":
            page = int(page)
            offset = ((page - 1) * 5)
            if (total_posts - offset) >  limit:
                nxt = (page + 1)
                prv = (page - 1)
            else:
                prv = (page - 1)
        else:
            offset = 0
            nxt = 2

        #Define what post show on blog page
        posts = get_posts(limit, offset)

        t = jinja_env.get_template("/blog.html")
        content = t.render(posts = posts, page = str(page), prv = str(prv), nxt = str(nxt))
        self.response.write(content)

class ViewPostHandler(webapp2.RequestHandler):
        def get(self, id):
            id = int(id)

            #Check to see if blog post exist in Post db
            post = Post.get_by_id(id)
            error = ""

            if post:
                t = jinja_env.get_template("/blog_post.html")
                content = t.render(post = post)
                self.response.write(content)
            else:
                error = "Unfortunately there is no blog post with that ID."
                t = jinja_env.get_template("/blog_post.html")
                content = t.render(post = post, error = error)
                self.response.write(content)


app = webapp2.WSGIApplication([
    ('/newpost', MakePostHandler),
    ('/blog', BlogHandler),
    webapp2.Route('/blog/<id:\d+>', ViewPostHandler)
], debug=True)
