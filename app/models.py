from . import db, login_manager
from datetime import datetime
from werkzeug.security import generate_password_hash,check_password_hash
from flask_login import UserMixin
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask import current_app
import hashlib

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
    email_hash = db.Column(db.String(64))
    confirmed = db.Column(db.Boolean, default=False)
    password_hash = db.Column(db.String(128))
    todos = db.relationship('Todo',backref='user')
    from_viewers = db.relationship('Follow',
                                foreign_keys=[Follow.from_id],
                                backref=db.backref('from_user', lazy='joined'),
                                cascade='all, delete-orphan',
                                lazy='dynamic')
    to_viewers = db.relationship('Follow',
                                foreign_keys=[Follow.to_id],
                                backref=db.backref('to_user', lazy='joined'),
                                cascade='all, delete-orphan',
                                lazy='dynamic')
    def compute_email_hash(self):
        self.email_hash = hashlib.md5(self.email.lower().encode('utf-8')).hexdigest()

    def generate_confirmation_token(self, expiration=3600):
        s = Serializer(current_app.config['SECRET_KEY'], expiration)
        return s.dumps({'confirm': self.id}).decode('utf-8')

    def confirm(self, token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token.encode('utf-8'))
        except:
            return False
        if data.get('confirm') != self.id:
            return False
        self.confirmed = True
        db.session.add(self)
        return True

    def follow(self, user):
        if not self.is_following(user):
            f = Follow( from_user = self, to_user = user )
            db.session.add(f)
            db.session.commit()

    def unfollow(self, user):
        f = self.from_viewers.filter_by(to_id=user.id).first()
        if f:
            db.session.delete(f)
            db.session.commit()

    def is_following(self, user):
        if user.id is None:
            return False
        return self.from_viewers.filter_by(to_id=user.id).first() is not None

    def is_followed_by(self, user):
        if user.id is None:
            return False
        return self.to_viewers.filter_by(from_id=user.id).first() is not None

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
