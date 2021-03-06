from flask import render_template, redirect, url_for
from . import main
from ..models import Todo, User, Comment
from .forms import NameForm, TodoEditForm, EditProfileForm, CommentForm
from .. import db, mail
from datetime import datetime
from flask_login import current_user

# test mail
from flask_mail import Message

@main.route('/')
def index():
    return  render_template( 'index.html', current_time=datetime.utcnow() )

@main.route('/profile')
def profile():
    return render_template('profile.html')

@main.route('/edit_profile', methods=['GET', 'POST'])
def edit_profile():
    form = EditProfileForm()
    if form.validate_on_submit():
        current_user.about_me = form.about_me.data
        db.session.add(current_user)
        db.session.commit()
        return redirect(url_for('main.profile'))
    return render_template('edit_profile.html', form=form)

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
    user = User.query.get_or_404(int(user_id))
    todos = Todo.getByUserId(user_id)
    return render_template( 'todos.html', user = user, todos = todos)

@main.route('/todos/detail/<id>', methods=['GET', 'POST'])
def todo_detail(id):
    todo = Todo.query.get_or_404(int(id))
    form = CommentForm()
    if form.validate_on_submit():
        content = form.comment.data
        Comment.add(current_user, todo, content)
        redirect(url_for('main.todo_detail', id=id))
    return render_template('todo_detail.html', todo = todo, form=form)

@main.route('/todos/edit/<id>', methods=['GET', 'POST'])
def todo_edit(id):
    form = TodoEditForm()
    todo = Todo.query.get_or_404(int(id))
    if form.validate_on_submit():
        todo.name = form.name.data
        db.session.add(todo)
        db.session.commit()
        return redirect(url_for('main.todoByUser', user_id=todo.user.id))
    return render_template('todo_edit.html', todo = todo, form = form)

@main.route('/todos/del/<id>')
def delTodo(id):
    Todo.delete(id)
    return redirect(url_for('main.todoByUser', user_id = current_user.id))

@main.route('/names/<name>')
def name( name ):
    return render_template( 'name.html', name = name )

@main.route('/add', methods=['GET', 'POST'])
def add():
    form = NameForm()
    if form.validate_on_submit():
        Todo.add(form.name.data, current_user)
        return redirect(url_for('main.todoByUser', user_id = current_user.id))
    return render_template( 'add.html', form = form )

@main.route('/user_info/<id>')
def userInfo(id):
    user = User.query.get_or_404(int(id))
    return render_template('user_info.html',
                            user = user,
                            followers = user.from_viewers.all())

@main.route('/follow/<user_id>')
def follow(user_id):
    user = User.query.get_or_404(int(user_id))
    if user is not None:
        current_user.follow(user)
    return redirect(url_for('.users'))

@main.route('/unfollow/<user_id>')
def unfollow(user_id):
    user = User.query.get_or_404(int(user_id))
    if user is not None:
        current_user.unfollow(user)
    return redirect(url_for('.users'))


@main.app_errorhandler(404)
def page_not_found(e):
    return render_template('404.html')

@main.app_errorhandler(500)
def internal_server_error(e):
    print(e)
    print(type(e))
    return render_template('500.html')




#######################
# test email
@main.route('/test_mail')
def test_mail():
    msg = Message('test_mail', sender='', recipients=[''])
    msg.body='test body'
    msg.html='html'
    mail.send(msg)
    return redirect(url_for('.index'))
