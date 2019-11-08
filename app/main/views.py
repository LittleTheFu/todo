from flask import render_template, redirect, url_for
from . import main
from ..models import Todo, User
from .forms import NameForm
from .. import db
from datetime import datetime
from flask_login import current_user

@main.route('/')
def index():
    return  render_template( 'index.html', current_time=datetime.utcnow() )

@main.route('/profile')
def profile():
    return render_template('profile.html')

@main.route('/users')
def users():
    users = User.query.all()
    return render_template( 'users.html', users = users )

@main.route('/users/del/<id>')
def delUser(id):
    User.delete(id)
    return redirect(url_for('.users'))

@main.route('/todos')
def todos():
    todos = Todo.query.all()
    return render_template( 'todos.html', todos = todos )

@main.route('/todos/<user_id>')
def todoByUser(user_id):
    todos = Todo.getByUserId(user_id)
    canEdit = False
    if ( current_user is not None ) and ( current_user.id == int(user_id) ):
        canEdit = True
    return render_template( 'todos.html', user_id = user_id, todos = todos, canEdit = canEdit )

@main.route('/todos/del/<id>')
def delTodo(id):
    Todo.delete(id)
    return redirect(url_for('.todoByUser', user_id = current_user.id))

@main.route('/names/<name>')
def name( name ):
    return render_template( 'name.html', name = name )

@main.route('/add', methods=['GET', 'POST'])
def add():
    form = NameForm()
    if form.validate_on_submit():
        Todo.add(form.name.data, current_user)
        return redirect(url_for('.todoByUser', user_id = current_user.id))
    return render_template( 'add.html', form = form )

@main.route('/user_info/<id>')
def userInfo(id):
    user = User.query.get(int(id))
    return render_template('user_info.html', id = user.id, email = user.email)
