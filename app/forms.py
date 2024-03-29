from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired
from werkzeug.utils import secure_filename
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField, IntegerField, SelectField
from wtforms.validators import DataRequired, Optional, ValidationError
import app
from app.models import Post

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
  parent_slug = StringField('Enter slug of parent post',validators=[Optional()])
  featured_img = StringField('Enter featured image name', validators=[Optional()])
  status = SelectField('Draft/Publish', choices=[(0,'draft'),(1,'publish')])
  read_more_text = StringField('Enter text for Read More')
  
  def __init__(self, original_title, *args, **kwargs):
    super(PostForm, self).__init__(*args, **kwargs)
    self.original_title = original_title
    
  def validate_title(self, title):
    if title.data != self.original_title:
      post = Post.query.filter_by(title=self.title.data).first()
      if post is not None:
        raise ValidationError('Please use a different title.')

class EmptyForm(FlaskForm):
  submit = SubmitField('Delete')

class UploadForm(FlaskForm):
  file = FileField('File', validators=[FileRequired()])
  submit = SubmitField('Upload')

class SetFeaturedForm(FlaskForm):
  featured_list = []
  type = SelectField('Select featured type', choices=[('stories', 'stories'),
    ('books', 'books'), ('experiments', 'experiments'), ('questions', 'questions'),
    ('scientists', 'scientists'), ('weird-ideas', 'weird-ideas'),
    ('history-and-science-teaching', 'history-and-science-teaching'),
    ('instruments', 'instruments')])
  slug = StringField('Enter post slug', validators=[DataRequired()])
  submit = SubmitField('Submit')                    