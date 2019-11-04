from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField

class NameForm(FlaskForm):
    name = StringField('What is your name?')
    submit = SubmitField('Submit')
