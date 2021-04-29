from datetime import datetime
from dateutil import parser
import enum
from sqlalchemy.orm import synonym, validates

from app import db


class Base:
    def commit(self):
        try:
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            raise e

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
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(128))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    todo_tasks = db.relationship("TodoTask", backref="todo_list", lazy="dynamic")

    def __init__(self, title=None):
        self.title = title or "untitled"

    @validates('title')
    def validate_title_length(self, key, title):
        assert len(title) <= 128
        return title

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "created_at": self.created_at,
            "todo_tasks": [todo.to_dict() for todo in self.todo_tasks],
        }


class TaskStatus(enum.Enum):
    PENDING = 1
    DONE = 2


class TodoTask(db.Model, Base):
    __tablename__ = "todo_task"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(64))
    description = db.Column(db.String(128))
    _status = db.Column("status", db.Enum(TaskStatus), default=TaskStatus.PENDING.name)
    todo_list_id = db.Column(db.Integer, db.ForeignKey("todo_list.id"))
    _due_at = db.Column("due_at", db.DateTime, default=None)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __init__(self, title, description, todo_list_id, due_at):
        self.title = title
        self.description = description
        self.todo_list_id = todo_list_id
        self.due_at = due_at

    @validates('title')
    def validate_title_length(self, key, title):
        assert len(title) <= 64
        return title

    @validates('description')
    def validate_description_length(self, key, description):
        assert len(description) <= 128
        return description

    @property
    def due_at(self):
        return self._due_at

    @due_at.setter
    def due_at(self, val):
        if isinstance(val, datetime):
            self._due_at = val
        elif isinstance(val, str):
            self._due_at = parser.parse(val)
        else:
            raise NotImplementedError

    due_at = synonym("_due_at", descriptor=due_at)  # todo: another way to declare

    @property
    def status(self):
        if self._status:
            return self._status.name
        else:
            return TaskStatus.PENDING.name

    @status.setter
    def status(self, val):
        if val == TaskStatus.PENDING.name:
            self._status = TaskStatus.PENDING.name
        elif val == TaskStatus.DONE.name:
            self._status = TaskStatus.DONE.name
        else:
            raise NotImplementedError

    status = synonym("_status", descriptor=status)  # todo: another way to declare

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'status': self.status,
            'todo_list_id': self.todo_list_id,
            'created_at': self.created_at,
            'due_at': self.due_at,
        }