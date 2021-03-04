from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField, IntegerField, SelectField
from wtforms.validators import DataRequired, Optional

class LoginForm(FlaskForm):
  username = StringField('Username', validators=[DataRequired()])
  password = PasswordField('Password', validators=[DataRequired()])
  remember_me = BooleanField('Remember Me')
  submit = SubmitField('Sign In')

class PostForm(FlaskForm):
  title = StringField('Title', validators=[DataRequired()])
  post = TextAreaField('Write your post', validators=[DataRequired()])
  submit = SubmitField('Submit')
  add_remove_parent = SelectField('Add/Remove Parent', choices=[(0,'None'),(1,'Add'),(2,'Remove')], default=0)
  parent_id = IntegerField('Enter id of parent post',validators=[Optional()])  
    