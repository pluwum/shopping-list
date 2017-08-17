from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField
from wtforms import PasswordField
from wtforms.validators import DataRequired, EqualTo


class LoginForm(FlaskForm):
    email = StringField('email', validators=[DataRequired()])
    password = StringField('password', validators=[DataRequired()])
    remember_me = BooleanField('remember_me', default=False)


class RegistrationForm(FlaskForm):
    first_name = StringField('first_name', validators=[DataRequired()])
    last_name = StringField('last_name', validators=[DataRequired()])
    email = StringField('password', validators=[DataRequired()])
    password = PasswordField('New Password', validators=[
                             DataRequired(),
                             EqualTo(
                                 'repassword',
                                 message='Passwords must match')])
    repassword = PasswordField('Confirm Password')
