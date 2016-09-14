import webapp2
import os
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

class Home(Handler):
    def get(self):
        self.render("home.html")


class Post(db.Model):
    blog_title = db.StringProperty(required = True)
    blog_text = db.TextProperty(required = True)
    created = db.DateTimeProperty(auto_now_add = True)



class NewPost(Handler):
    def get(self):
        self.render("newpost.html")

    def post(self):
        blog_title = self.request.get("blog_title")
        blog_text = self.request.get("blog_text")

        if blog_title and blog_text:
            error = "Fields cannot be empty"
        p = Post(blog_title = blog_title, blog_text = blog_text)
        p.put()
        message = "Blog was successfully saved!"
        self.redirect('/')

class History(Handler):
    def post(self):
        posts = "SELECT * from Post" "ORDER BY created" "LIMIT 5"
        self.render("blog.html")

app = webapp2.WSGIApplication([
    ('/', Home),
    ('/blog', History),
    ('/newpost', NewPost)
], debug = True)
