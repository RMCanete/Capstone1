from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField
from wtforms.validators import DataRequired,Length

class UserAddForm(FlaskForm):
    """Form to add user"""

    username = StringField('Username', validators=[DataRequired()])
    email = StringField('E-mail', validators=[DataRequired()])
    password = PasswordField('Password', validators=[Length(min=7)])

class LoginForm(FlaskForm):
    """Login form"""

    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[Length(min=7)])

class CommentForm(FlaskForm):
    """Form for adding/editing comments"""

    comment = TextAreaField('text', validators=[DataRequired()])