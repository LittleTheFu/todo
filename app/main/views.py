from flask import render_template, redirect, url_for
from . import main
from ..models import Todo
from .forms import NameForm
from .. import db

@main.route('/')
def index():
    return  render_template( 'index.html' )

@main.route('/todos')
def todo():
    todos = Todo.query.all()
    print(todos)
    return render_template( 'todo.html', todos = todos )

@main.route('/todos/del/<id>')
def delTodo(id):
    todo = Todo.query.filter_by(id=id).first()
    if todo:
        db.session.delete(todo)
        db.session.commit()
    return redirect(url_for('.todo'))

@main.route('/names/<name>')
def name( name ):
    return render_template( 'name.html', name = name )

@main.route('/add', methods=['GET', 'POST'])
def add():
    form = NameForm()
    if form.validate_on_submit():
        todo = Todo()
        todo.name = form.name.data
        db.session.add(todo)
        db.session.commit()
        return redirect('/todos')
    return render_template( 'add.html', form = form )
