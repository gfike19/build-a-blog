import webapp2
import os
import re
import jinja2
from google.appengine.ext import db

template_dir = os.path.join(os.path.dirname(__file__),'templates')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir), autoescape = True)
# p_id = 0

class Handler(webapp2.RequestHandler):
    def write(self, *a, **kw):
        self.response.out.write(*a, **kw)

    def render_str(self, template, **params):
        t = jinja_env.get_template(template)
        return t.render(params)

    def render (self, template, **kw):
        self.write(self.render_str(template, **kw))


class Post(db.Model):
    blog_title = db.StringProperty(required = True)
    blog_text = db.TextProperty(required = True)
    created = db.DateTimeProperty(auto_now_add = True)

class ViewPostHandler(Handler):
    def get(self, id):
        post = Post.get_by_id(int(id))
        if post:
            # query = Post.all().order('-author')
            # post = db.GqlQuery("SELECT * FROM Post WHERE ID == p_id")
            # title = db.GqlQuery("SELECT blog_title FROM Post WHERE ID == p_id")
            # text = db.GqlQuery("SELECT blog_text FROM Post WHERE ID == p_id")
            # self.render("view-single-post.html", title = title, text = text)
            self.render("view-single-post.html", post = post)
        else:
            error = "Blog may not have been stored"
            self.render("view-single-post.html", error = error)

class NewPost(Handler):

    def get(self):
        self.render("newpost.html")

    def post(self):
        blog_title = self.request.get("blog_title")
        blog_text = self.request.get("blog_text")

        if blog_title and blog_text:
            p = Post(blog_title = blog_title, blog_text = blog_text)
            p.put()
            p_id = p.key().id()
            self.redirect("/blog/%s" % p_id)
        else:
            error = "Fields cannot be empty"
            self.render("newpost.html", error = error, blog_title = blog_title, blog_text = blog_text)

class History(Handler):
    def get(self):
        posts = db.GqlQuery("SELECT * from Post ORDER BY created DESC LIMIT 5")
        self.render("blog.html", posts = posts)

class Home(Handler):
    def get(self):
        self.render("home.html")



app = webapp2.WSGIApplication([('/', Home),
    ('/blog/newpost', NewPost), #new post
    webapp2.Route('/blog/<id:\d+>', ViewPostHandler),
    ('/blog', History) #mainpage
], debug = True)
#
