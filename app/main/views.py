from flask import render_template
from . import main

@main.route('/')
def index():
    return  render_template( 'index.html' )

@main.route('/hello')
def hello():
    return render_template( 'hello.html' )

@main.route('/names/<name>')
def name( name ):
    return render_template( 'name.html', name = name )
