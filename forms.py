from flask_wtf import FlaskForm
from wtforms import (
    StringField,
    PasswordField,
    TextAreaField,
    SubmitField,
    DateField,
    SelectMultipleField,
    IntegerField,
    FloatField,
)
from wtforms.validators import DataRequired, Email

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

class RegisterForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Register')

class ContactForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    message = TextAreaField('Message', validators=[DataRequired()])
    submit = SubmitField('Send')

class EventForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    date = DateField('Date', validators=[DataRequired()])
    description = TextAreaField('Description', validators=[DataRequired()])
    submit = SubmitField('Add')

class ProfileForm(FlaskForm):
    first_name = StringField('First Name')
    last_name = StringField('Last Name')
    graduation_year = IntegerField('Graduation Year')
    gpa = FloatField('GPA')
    team = StringField('Team')
    school = StringField('School')
    club = StringField('Club')
    height = StringField('Height')
    weight_class = StringField('Weight Class')
    colleges = SelectMultipleField('Interested Colleges', coerce=int)
    submit = SubmitField('Save')

class MatchForm(FlaskForm):
    opponent = StringField('Opponent', validators=[DataRequired()])
    date = DateField('Date', validators=[DataRequired()])
    description = TextAreaField('Description')
    submit = SubmitField('Add')
