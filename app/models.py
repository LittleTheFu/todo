from . import db
from datetime import datetime

class Todo(db.Model):
    __tablename__ = 'todos'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    create_date = db.Column(db.Date)

    @staticmethod
    def add(name):
        todo = Todo()
        todo.name = name
        todo.create_date = datetime.utcnow()
        print("@@@@@@@@@@@@@@@@@@")
        print(todo.create_date)
        db.session.add(todo)
        db.session.commit()

    @staticmethod
    def delete(id):
        todo = Todo.query.filter_by(id=id).first()
        if todo:
            db.session.delete(todo)
            db.session.commit()
        pass
