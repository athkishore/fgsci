from datetime import datetime, timedelta
import unittest
from app import app, db
from app.models import User, Post

class PostModelCase(unittest.TestCase):
  def setUp(self):
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite://'
    db.create_all()
    
  def tearDown(self):
    db.session.remove()
    db.drop_all()
    
  def test_password_hashing(self):
    u = User(username='susan')
    u.set_password('cat')
    self.assertFalse(u.check_password('dog'))
    self.assertTrue(u.check_password('cat'))
    
  def test_post_rel(self):
    u = User(username='admin', email='kishore.asok@gmail.com')
    db.session.add(u)
    p1 = Post(title='Test post 1', body='test body 1', author = u)
    p2 = Post(title='Test post 2', body='test body 2', author = u)
    db.session.add(p1)
    db.session.add(p2)
    db.session.commit()
    self.assertEqual(p1.child_posts.all(), [])
    self.assertEqual(p1.parent_posts.all(), [])
    
    p2.make_child_of(p1)
    db.session.commit()
    self.assertTrue(p2.is_child_of(p1))
    self.assertEqual(p1.child_posts.count(), 1)
    self.assertEqual(p1.child_posts.first().title, 'Test post 2')
    self.assertEqual(p2.parent_posts.count(), 1)
    self.assertEqual(p2.parent_posts.first().title, 'Test post 1')
    
    p2.remove_parent(p1)
    db.session.commit()
    self.assertFalse(p2.is_child_of(p1))
    self.assertEqual(p2.parent_posts.count(), 0)
    self.assertEqual(p1.child_posts.count(), 0)
    
  def test_child_posts(self):
    u = User(username = 'admin', email='kishore.asok@gmail.com')
    db.session.add(u)
    
    now = datetime.utcnow()
    p1 = Post(title='Test post 1', body='test body 1', author=u,
      timestamp=now + timedelta(seconds=1))
    p2 = Post(title='Test post 2', body='test body 2', author=u,
      timestamp=now + timedelta(seconds=4))
    p3 = Post(title='Test post 3', body='test body 3', author=u,
      timestamp=now + timedelta(seconds=3))
    p4 = Post(title='Test post 4', body='test body 4', author=u,
      timestamp=now + timedelta(seconds=2))
    db.session.add_all([p1, p2, p3, p4])
    db.session.commit()
    
    p1.make_child_of(p2)
    p1.make_child_of(p4)
    p2.make_child_of(p3)
    p3.make_child_of(p4)
    db.session.commit()
    
    f1 = p1.child_posts.all()
    f2 = p2.child_posts.all()
    f3 = p3.child_posts.all()
    f4 = p4.child_posts.all()
    self.assertEqual(f1, [])
    self.assertEqual(f2, [p1])
    self.assertEqual(f3, [p2])
    self.assertEqual(f4, [p1, p3])

if __name__ == '__main__':
  unittest.main(verbosity=2)
  