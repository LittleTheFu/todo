from . import db, login_manager
from datetime import datetime
from werkzeug.security import generate_password_hash,check_password_hash
from flask_login import UserMixin

class Follow(db.Model):
    from_id = db.Column(db.Integer,
                        db.ForeignKey('users.id'),
                        primary_key=True)
    to_id = db.Column(db.Integer,
                        db.ForeignKey('users.id'),
                        primary_key=True)

class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(64),unique=True,index=True)
    password_hash = db.Column(db.String(128))
    todos = db.relationship('Todo',backref='user')
    from_ids = db.relationship('Follow',
                                foreign_keys=[Follow.from_id],
                                backref='from',
                                cascade='all, delete-orphan')
    to_ids = db.relationship('Follow',
                                foreign_keys=[Follow.to_id],
                                backref='to',
                                cascade='all, delete-orphan')

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self,password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self,password):
        return check_password_hash(self.password_hash,password)

    @staticmethod
    def delete(id):
        user = User.query.filter_by(id=id).first()
        if user:
            db.session.delete(user)
            db.session.commit()
        pass

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class Todo(db.Model):
    __tablename__ = 'todos'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    create_date = db.Column(db.Date)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    @staticmethod
    def add(name, user):
        todo = Todo(user=user)
        todo.name = name
        todo.create_date = datetime.utcnow()
        print('@@@@@@@@@@')
        print(todo.user.id)
        print(todo.user.email)
        print(todo.user.password_hash)
        db.session.add(todo)
        db.session.commit()

    @staticmethod
    def delete(id):
        todo = Todo.query.filter_by(id=id).first()
        if todo:
            db.session.delete(todo)
            db.session.commit()

    @staticmethod
    def getByUserId(id):
        return Todo.query.join(User, Todo.user_id==id)
