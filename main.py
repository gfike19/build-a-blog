import webapp2
import os
import re
import jinja2

from google.appengine.ext import db

template_dir = os.path.join(os.path.dirname(__file__),'templates')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir), autoescape = True)

class Handler(webapp2.RequestHandler):
    def write(self, *a, **kw):
        self.response.out.write(*a, **kw)

    def render_str(self, template, **params):
        t = jinja_env.get_template(template)
        return t.render(params)

    def render (self, template, **kw):
        self.write(self.render_str(template, **kw))

# class Home(Handler):
#     def get(self):
#         self.render("home.html")
#
#     def post(self):
#         link = str(self.request.get("link"))
#         if link == "Create a new blog":
#             self.redirect("/newpost")
#         if link == "View older blogs":
#             self.redirect("/blog")
#             self.e


class Post(db.Model):
    blog_title = db.StringProperty(required = True)
    blog_text = db.TextProperty(required = True)
    created = db.DateTimeProperty(auto_now_add = True)

# class ViewPostHandler(Handler):
#     def get(self, id):
#         pass



class NewPost(Handler):
    def render_newblog(self, error = "", blog_title = "", blog_text = ""):
        self.render("newpost.html", error = error, blog_title = blog_title, blog_text = blog_text)

    def get(self):
        self.render_newblog()

    def post(self):
        blog_title = self.request.get("blog_title")
        blog_text = self.request.get("blog_text")

        if blog_title and blog_text:
            p = Post(blog_title = blog_title, blog_text = blog_text)
            newpost = p.put()
            # Post.put()
            # p.put()
            # Post.put(p)
            # message = "Blog was successfully saved!"
            # self.redirect('/blog')
        else:
            error = "Fields cannot be empty"
            self.render_newblog(blog_title, blog_text, error)

class History(Handler):
    def post(self):
        posts = db.GqlQuery("SELECT post from Post ORDER BY created LIMIT 5")
        self.render("blog.html")

# webapp2.Route('/blog/<id:\d+>', ViewPostHandler)

app = webapp2.WSGIApplication([
    # ('/', Home),
    ('/', NewPost),
    ('/blog', History)
], debug = True)
