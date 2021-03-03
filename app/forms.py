from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField, IntegerField
from wtforms.validators import DataRequired

class LoginForm(FlaskForm):
  username = StringField('Username', validators=[DataRequired()])
  password = PasswordField('Password', validators=[DataRequired()])
  remember_me = BooleanField('Remember Me')
  submit = SubmitField('Sign In')

class PostForm(FlaskForm):
  title = StringField('Title', validators=[DataRequired()])
  post = TextAreaField('Write your post', validators=[DataRequired()])
  submit = SubmitField('Submit')
  make_child_of = IntegerField('Enter id of parent post')
  remove_parent = IntegerField('Enter id of parent post')
  
    