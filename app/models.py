from datetime import datetime
from app import db

class User(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  username = db.Column(db.String(64), index=True, unique=True)
  email = db.Column(db.String(120), index=True, unique=True)
  password_hash = db.Column(db.String(128))
  posts = db.relationship('Post', backref='author', lazy='dynamic')
  
  def __repr__(self):
    return '<User {}>'.format(self.username)
    
class Post(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  body = db.Column(db.Text)
  timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
  user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
  category = db.Column(db.String(64), db.ForeignKey('category.id'))
  
  def __repr__(self):
    return '<Post {}>'.format(self.body)

class Category(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(64), index=True, unique=True)
  posts = db.relationship('Post', backref='category', lazy='dynamic')  
  
  def __repr__(self):
    return '<Category {}>'.format(self.name)
    