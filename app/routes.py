from flask import render_template, flash, redirect, url_for, request
from app import app, db
from app.forms import LoginForm, PostForm, EmptyForm
from app.models import User, Post
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.urls import url_parse

@app.route('/')
@app.route('/index')
#@login_required
def index():
  #user = {'username':'admin'}
  posts = Post.query.order_by(Post.timestamp.desc()).all()
  return render_template('index.html', title='Home', posts=posts[0:1])

@app.route('/all-posts')
#@login_required
def all_posts():
  #user = {'username':'admin'}
  posts = Post.query.order_by(Post.timestamp.desc()).all()
  return render_template('all_posts.html', title='Home', posts=posts)

  
@app.route('/login', methods=['GET', 'POST'])
def login():
  if current_user.is_authenticated:
    return redirect(url_for('index'))
  form = LoginForm()
  if form.validate_on_submit():
    user = User.query.filter_by(username=form.username.data).first()
    if user is None or not user.check_password(form.password.data):
      flash('Invalid username or password')
      return redirect(url_for('login'))
    login_user(user, remember=form.remember_me.data)
    next_page = request.args.get('next')
    if not next_page or url_parse(next_page).netloc != '':
      next_page = url_for('index')
    return redirect(next_page)
  return render_template('login.html', title='Sign In', form=form)
 
@app.route('/logout')
def logout():
  logout_user()
  return redirect(url_for('index'))

@app.route('/edit-post/<post_slug>', methods=['GET', 'POST'])
@login_required
def edit_post(post_slug):
  post = Post.query.filter_by(slug=post_slug).first_or_404()
  form = PostForm(post.title)
  if form.validate_on_submit():
    post.title = form.title.data
    post.set_slug()
    post.body = form.post.data
    if form.parent_slug.data:
      parent = Post.query.filter_by(slug=form.parent_slug.data).first_or_404()
      if int(form.add_remove_parent.data) == 1 and not post.is_child_of(parent):
        post.make_child_of(parent)
        flash('Added parent {}'.format(parent))
      elif int(form.add_remove_parent.data) == 2 and post.is_child_of(parent):
        post.remove_parent(parent)
        flash('Removed parent {}'.format(parent))
    db.session.commit()
    flash('Your changes have been saved.')
    return redirect(url_for('index'))    
  elif request.method == 'GET':
    form.title.data = post.title
    form.post.data = post.body
  return render_template("edit_post.html", title="Edit Post", form=form,
    post = post)

@app.route('/create-post', methods=['GET', 'POST'])
@login_required
def create_post():
  form = PostForm('')
  if form.validate_on_submit():
    post = Post(title=form.title.data, body=form.post.data, author=current_user)
    post.set_slug()
    db.session.add(post)
    db.session.commit()
    flash('Your post is now live!')
    return redirect(url_for('index'))
  return render_template("create_post.html", title="Create Post", form=form)   
  
@app.route('/view-post/<post_slug>')
def view_post(post_slug):
  post = Post.query.filter_by(slug=post_slug).first_or_404()
  form = EmptyForm()
  return render_template("view_post.html", title=post.title, post=post, form=form)     
  
@app.route('/delete-post/<post_slug>', methods=['GET', 'POST'])
@login_required
def delete_post(post_slug):
  post = Post.query.filter_by(slug=post_slug).first_or_404()
  posts = Post.query.all()
  for child_post in posts:
    if child_post.is_child_of(post):
      child_post.remove_parent(post)
  for parent_post in posts:
    if post.is_child_of(parent_post):
      post.remove_parent(parent_post)
  db.session.delete(post)
  db.session.commit()
  return redirect(url_for('index'))
  