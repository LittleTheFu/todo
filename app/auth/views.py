from flask import render_template
from . import auth
from .forms import LoginForm
from flask_login import login_user
from ..models import User

@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is not None and user.verify_password(form.password.data):
            login_user(user, form.remember_me.data)
        print("@@@@@@@@@@@@@@@@")
        print("success login")
    return render_template('auth/login.html', form=form)
