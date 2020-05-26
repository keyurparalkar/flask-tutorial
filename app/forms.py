from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError
from app.models import User

class LoginForm(FlaskForm):
    username = StringField('Username',validators=[DataRequired()])
    password = PasswordField('Password',validators=[DataRequired()])
    remember_me = BooleanField('Remember me')
    submit = SubmitField('Sign In')


class RegistrationForm(FlaskForm):
    username = StringField('Username',validators=[DataRequired()])
    email = StringField('Email Address', validators=[DataRequired(),Email()])
    password = PasswordField('Password',validators=[DataRequired()])
    password2 = PasswordField('Confirm your password',validators=[DataRequired(),EqualTo('password')])

    submit = SubmitField('Register')

    def validate_username(self,username):
        user = User.query.filter_by(username=username.data).first()
        if(user is not None):
            raise ValidationError('Username already exists. Please enter different username')

    def validate_email(self,email):
        email_id = User.query.filter_by(email=email.data).first()
        if(email_id is not None):
            raise ValidationError('Email Id already existing. Please enter a different email id')
        
class ProfileEditForm(FlaskForm):
    username = StringField('Username')
    about_me = StringField('About Me')
    submit = SubmitField('Edit Profile')
