from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField

class NameForm(FlaskForm):
    name = StringField('todo : ')
    submit = SubmitField('Submit')

class TodoEditForm(FlaskForm):
    name = StringField('name : ')
    submit = SubmitField('Submit')
    # cancel = SubmitField('Cancel')

class EditProfileForm(FlaskForm):
    about_me = StringField('about me : ')
    submit = SubmitField('Submit')
    # cancel = SubmitField('Cancel')

class CommentForm(FlaskForm):
    comment = StringField('comment : ')
    submit = SubmitField('Submit')
