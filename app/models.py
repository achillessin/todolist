from datetime import datetime
import enum
from sqlalchemy.orm import synonym

from app import db


class Base:
    def commit(self):
        try:
            db.session.commit()
        except Exception:
            db.session.rollback()

    def update(self, attrs_dict):
        for key, value in attrs_dict.iteritems():
            if hasattr(self, key):
                setattr(self, key, value)
        self.save()

    def save(self):
        db.session.add(self)
        self.commit()
        db.session.refresh(self)
        return self

    def delete(self):
        db.session.delete(self)
        self.commit()


class TodoList(db.Model, Base):
    __tablename__ = "todo_list"
    id = db.Column(db.Integer, primary_key=True)
    _title = db.Column("title", db.String(128))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    deleted_at = db.Column(db.DateTime, default=None)
    todo_tasks = db.relationship("TodoTask", backref="todo_list", lazy="dynamic")

    def __init__(self, title=None):
        self.title = title or "untitled"

    @property
    def title(self):
        return self._title

    @title.setter # todo use a validate instead
    def title(self, title):
        if not len(title, 128):
            raise ValueError(f"{title} is not a valid title")
        self._title = title

    title = synonym("_title", descriptor=title) # todo: another way to declare

    def to_dict(self):
        return {
            "title": self.title,
            "created_at": self.created_at,
            "deleted_at": self.deleted_at,
            "todo_tasks": [todo.to_dict() for todo in self.todo_tasks],
        }


class TaskStatus(enum.Enum):
    PENDING = 1
    DONE = 2


class TodoTask(db.Model, Base):
    __tablename__ = "todo_task"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(64)) # todo: why?
    description = db.Column(db.String(128)) #todo: why? how to control size on UI
    status = db.Column(db.Enum(TaskStatus), default=TaskStatus.PENDING.value, server_default=TaskStatus.PENDING.value)
    todo_list_id = db.Column(db.Integer, db.ForeignKey("todo_list.id"))
    due_at = db.Column(db.DateTime, default=None)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    deleted_at = db.Column(db.DateTime, default=None)

    def __init__(self, title, description, todo_list_id, due_at):
        self.title = title
        self.description = description
        self.todo_list_id = todo_list_id
        self.due_at = due_at

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'status': self.status.value,
            'todo_list_id': self.todo_list_id,
            'created_at': self.created_at,
            'due_at': self.due_at,
        }