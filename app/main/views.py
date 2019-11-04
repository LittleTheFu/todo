from flask import render_template
from . import main
from ..models import Todo

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

@main.route('/add')
def add():
    return render_template('add.html')
