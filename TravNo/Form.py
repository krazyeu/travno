from flask_login import current_user
from flask_wtf import FlaskForm
from wtforms import StringField, FileField, PasswordField, SubmitField, BooleanField, DateField, SelectField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from wtforms.fields.html5 import DateField
from flask_wtf.file import FileField, FileAllowed
from TravNo import db
from TravNo.Models import User, Sub_User

class RegistrationForm(FlaskForm):
    depart= StringField("Departing", validators=[DataRequired()])
    arr = StringField("Arrival", validators=[DataRequired()])
    email = StringField("Email", validators=[DataRequired(), Email()])
    code = StringField("Code", validators=[DataRequired(), Length(min=4,max=4)])
    submit = SubmitField("Start Planing!")

class LoginForm(FlaskForm):
    iti_code = StringField("Itinerary Code", validators=[DataRequired()])
    code = PasswordField("Code", validators=[DataRequired()])
    remember = BooleanField("Remember Me")
    submit = SubmitField("Login")

class WhoForm(FlaskForm):
    name = StringField("Your Name please", validators=[DataRequired()])
    email = StringField("Email so we can send you the itinerary", validators=[DataRequired(), Email()])
    picture = FileField('Update Profile Picture', validators=[FileAllowed(['jpg', 'png'])])
    submit = SubmitField("Got it!")

class who_login(FlaskForm):
    choice = ('Vincent','Vincent'), ('Eunice', 'Eunice')
    whoyouare = SelectField("Tell us who you are!", choices=choice, validators=[DataRequired()])
    submit = SubmitField("Cool")

class SetupForm(FlaskForm):
    dt = DateField('DatePicker')
    flight_choice = ('yes', 'Yes, I have settled my flight'),\
                    ('no','No, What should I do?')
    accommodation_choice = ('yes', 'I have gotten all the necessary accommodation'),\
                           ('still', 'Still sorting some other accommodation'),\
                           ('no', 'I have not started to plan for accommodation')
    accommodation_style = ('bnb','Stay like a local'), ('hotel','Live Luxuriously'), ('surprise', 'I have no idea what I am looking for')
    start_travel = DateField("Let's GO!! ", validators=[DataRequired()])
    end_travel = DateField("I'm coming home....", validators=[DataRequired()])
    depart_airport = StringField("Departure Airport", validators=[DataRequired()])
    arrival_airport = StringField("Arrival Airport", validators=[DataRequired()])
    pax = StringField("How many friends joining??", validators=[DataRequired()])
    flight_tix = SelectField("Have you gotten your flight ticket?", choices=flight_choice, validators=[DataRequired()])
    accommodation = SelectField("What about your accommodation",choices=accommodation_choice, validators=[DataRequired()])
    style_accommodation = SelectField("How's your stay going to be like?",choices=accommodation_style, validators=[DataRequired()])
    submit = SubmitField("All done")

class TravelPlace(FlaskForm):
    location = StringField('Enter your attraction', validators=[DataRequired()])
    