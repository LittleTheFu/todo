from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField

class NameForm(FlaskForm):
    name = StringField('todo : ')
    submit = SubmitField('Submit')

class TodoEditForm(FlaskForm):
    name = StringField('name : ')
    submit = SubmitField('Submit')
