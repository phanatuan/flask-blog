from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextField, PasswordField, validators
from wtforms.validators import DataRequired, Email

class LoginForm(FlaskForm): 
    email = StringField('Email', validators=[DataRequired()] )
    password = PasswordField('Password', validators=[DataRequired()] )
    submit = SubmitField('Submit')

class AccountInfoForm(FlaskForm): 
    username = StringField('Username')
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Edit Info')