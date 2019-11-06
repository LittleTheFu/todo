from flask import render_template, redirect, url_for
from . import main
from ..models import Todo, User
from .forms import NameForm
from .. import db
from datetime import datetime

@main.route('/')
def index():
    return  render_template( 'index.html', current_time=datetime.utcnow() )

@main.route('/users')
def users():
    users = User.query.all()
    return render_template( 'user.html', users = users )

@main.route('/users/del/<id>')
def delUser(id):
    User.delete(id)
    return redirect(url_for('.users'))

@main.route('/todos')
def todo():
    todos = Todo.query.all()
    print(todos)
    return render_template( 'todo.html', todos = todos )

@main.route('/todos/del/<id>')
def delTodo(id):
    Todo.delete(id)
    return redirect(url_for('.todo'))

@main.route('/names/<name>')
def name( name ):
    return render_template( 'name.html', name = name )

@main.route('/add', methods=['GET', 'POST'])
def add():
    form = NameForm()
    if form.validate_on_submit():
        Todo.add(form.name.data)
        return redirect('/todos')
    return render_template( 'add.html', form = form )
