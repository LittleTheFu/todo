from . import main

@main.route('/')
def index():
    return  '<h1>Hello World!</h1>'

@main.route('/hello')
def hello():
    return '<h1>Hello</h1>'
