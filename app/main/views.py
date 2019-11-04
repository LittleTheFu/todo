from flask import render_template, redirect, url_for
from . import main
from ..models import Todo
from .forms import NameForm
from .. import db

@main.route('/')
def index():
    return  render_template( 'index.html' )

@main.route('/todos')
def hello():
    todos = Todo.query.all()
    print(todos)
    return render_template( 'hello.html', todos = todos )

@main.route('/names/<name>')
def name( name ):
    return render_template( 'name.html', name = name )

@main.route('/add', methods=['GET', 'POST'])
def add():
    form = NameForm()
    if form.validate_on_submit():
        todo = Todo()
        db.session.add(todo)
        db.session.commit()
        return redirect('/todos')
    return render_template( 'add.html', form = form )
