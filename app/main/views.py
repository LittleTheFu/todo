from . import main

@main.route('/')
def index():
    print("route_index")
    return  '<h1>Hello World!</h1>'
