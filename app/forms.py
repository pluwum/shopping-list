"""This file contains form class definations required to retrieve and display
data for the shopping list application
"""
from flask_wtf import FlaskForm
from wtforms import BooleanField, PasswordField, StringField
from wtforms.validators import DataRequired, EqualTo


class LoginForm(FlaskForm):
    """The Login form defines the contents of the user login interface form"""
    email = StringField('email', validators=[DataRequired()])
    password = PasswordField('password', validators=[DataRequired()])
    remember_me = BooleanField('remember_me', default=False)


class RegistrationForm(FlaskForm):
    """The Registration form defines the contents of the user registration
    form
    """
    first_name = StringField('first_name', validators=[DataRequired()])
    last_name = StringField('last_name', validators=[DataRequired()])
    email = StringField('password', validators=[DataRequired()])
    password = PasswordField('New Password', validators=[
                             DataRequired(),
                             EqualTo(
                                 'repassword',
                                 message='Passwords must match')])
    repassword = PasswordField('Confirm Password')


class CreateListForm(FlaskForm):
    """The CreateListForm defines the contents of the create new shopping list
     web form
    """
    name = StringField('name', validators=[DataRequired()])
    description = StringField('description', validators=[DataRequired()])
