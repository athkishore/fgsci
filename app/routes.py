from flask import render_template, flash, redirect, url_for, request
from app import app, db
from app.forms import LoginForm, PostForm
from app.models import User, Post
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.urls import url_parse

@app.route('/')
@app.route('/index')
#@login_required
def index():
  #user = {'username':'admin'}
  posts = Post.query.all()
  return render_template('index.html', title='Home', posts=posts)
  
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

@app.route('/edit-post/<post_id>', methods=['GET', 'POST'])
@login_required
def edit_post(post_id):
  post = Post.query.filter_by(id=int(post_id)).first_or_404()
  form = PostForm()
  if form.validate_on_submit():
    post.body = form.post.data
    db.session.commit()
    flash('Your changes have been saved.')
    return redirect(url_for('index'))    
  elif request.method == 'GET':
    form.post.data = post.body
  return render_template("edit_post.html", title="Edit Post", form=form,
    post = post)

@app.route('/create-post', methods=['GET', 'POST'])
@login_required
def create_post():
  form = PostForm()
  if form.validate_on_submit():
    post = Post(body=form.post.data, author=current_user)
    db.session.add(post)
    db.session.commit()
    flash('Your post is now live!')
    return redirect(url_for('index'))
  return render_template("create_post.html", title="Create Post", form=form)         