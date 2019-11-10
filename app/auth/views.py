from flask import render_template, redirect, url_for, flash
from . import auth
from .forms import LoginForm, RegistrationForm
from flask_login import login_user, logout_user
from ..models import User
from .. import db, mail
from flask_mail import Message
from flask_login import current_user

@auth.route('/confirm/<token>')
def confirm(token):
    if current_user.confirmed:
        return redirect(url_for('main.index'))
    if current_user.confirm(token):
        db.session.commit()
    return redirect(url_for('main.index'))

@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is not None and user.verify_password(form.password.data):
            login_user(user, form.remember_me.data)
            return redirect(url_for('main.index'))
    flash('Invalid email or password.')
    return render_template('auth/login.html', form=form)

@auth.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(email=form.email.data.lower(),
                    password=form.password.data)
        db.session.add(user)
        db.session.commit()
        token = user.generate_confirmation_token()
        msg = Message('test_mail', sender='LttLTheFu@hotmail.com', recipients=[form.email.data.lower()])
        msg.body=token
        address = url_for('auth.confirm', token=token)
        msg.html= 'http://127.0.0.1:5000' + address
        mail.send(msg)
        return redirect(url_for('auth.login'))
    return render_template('auth/register.html', form=form)

@auth.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('main.index'))
