from datetime import datetime
from app import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from app import login
from slugify import slugify

post_rel = db.Table('post_rel', 
  db.Column('parent_id', db.Integer, db.ForeignKey('post.id')),
  db.Column('child_id', db.Integer, db.ForeignKey('post.id'))
)

class User(UserMixin, db.Model):
  id = db.Column(db.Integer, primary_key=True)
  username = db.Column(db.String(64), index=True, unique=True)
  email = db.Column(db.String(120), index=True, unique=True)
  password_hash = db.Column(db.String(128))
  posts = db.relationship('Post', backref='author', lazy='dynamic')
  
  def __repr__(self):
    return '<User {}>'.format(self.username)
    
  def set_password(self, password):
    self.password_hash = generate_password_hash(password)
    
  def check_password(self, password):
    return check_password_hash(self.password_hash, password)
    
class Post(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  title = db.Column(db.String(128), index=True, unique=True)
  body = db.Column(db.Text)
  timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
  user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
  category = db.Column(db.Integer, db.ForeignKey('category.id'))
  slug = db.Column(db.String(128), index=True, unique=True)
  featured_img = db.Column(db.String(128))
  status = db.Column(db.Integer)
  read_more_text = db.Column(db.String(64))
  child_posts = db.relationship(
    'Post', secondary=post_rel,
    primaryjoin=(post_rel.c.parent_id == id),
    secondaryjoin=(post_rel.c.child_id == id),
    backref=db.backref('parent_posts', lazy='dynamic'), lazy='dynamic')
  
  def __repr__(self):
    return '<Post {}>'.format(self.body)
    
  def set_slug(self):
    self.slug = slugify(self.title)

  def make_child_of(self, post):
    if not self.is_child_of(post):
      self.parent_posts.append(post)
      
  def remove_parent(self, post):
    if self.is_child_of(post):
      self.parent_posts.remove(post)
      
  def is_child_of(self, post):
    return self.parent_posts.filter(
      post_rel.c.parent_id == post.id).count() > 0

#  def child_posts(self):
#    return Post.query.join(
#      post_rel, (post_rel.c.parent_id == Post.id)).filter(
#        post_rel.c.parent_id == self.id)

class Category(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(64), index=True, unique=True)
  posts = db.relationship('Post', backref='categ', lazy='dynamic')  
  
  def __repr__(self):
    return '<Category {}>'.format(self.name)

@login.user_loader
def load_user(id):
  return User.query.get(int(id))

class Featured(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  type = db.Column(db.String(32), index=True, unique=True)
  display = db.Column(db.String(128))
  post_id = db.Column(db.Integer, db.ForeignKey('post.id'))        