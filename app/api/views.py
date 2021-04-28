from flask import abort, request

from app.api import api
from app.models import TodoList, TodoTask


@api.route("/todolists/")
def get_todolists():
    todolists = TodoList.query.all()
    return {"todolists": [todolist.to_dict() for todolist in todolists]}


@api.route("/todolist/<int:todolist_id>/")
def get_todolist(todolist_id):
    todolist = TodoList.query.get_or_404(todolist_id)
    return todolist.to_dict()


@api.route("/todolist/", methods=["POST"])
def create_todolist():
    try:
        todolist = TodoList(title=request.json.get("title")).save()
        return todolist.to_dict(), 201
    except Exception as e:
        return str(e), 500


@api.route("/todolist/<int:todolist_id>/task", methods=["POST"])
def create_todolist_task(todolist_id):
    todolist = TodoList.query.get_or_404(todolist_id)
    try:
        todo = TodoTask(
            title=request.json.get("title"),
            description=request.json.get("description"),
            todo_list_id=todolist.id,
            due_at=request.json.get("due_at")
        ).save()
        return todo.to_dict(), 201
    except Exception as e:
        return str(e), 500


@api.route("/todolist/<int:todolist_id>/task/<int:task_id>/")
def get_task(todolist_id, task_id):
    todo = TodoTask.query.get_or_404(task_id)
    return todo.to_dict(), 201


@api.route("/todolist/<int:todolist_id>/task/<int:task_id>/", methods=["PUT"])
def update_task(todolist_id, task_id):
    todo = TodoTask.query.get_or_404(task_id)
    try:
        todo.title = request.json.get("title")
        todo.description = request.json.get("description")
        todo.due_at = request.json.get("due_at")
        todo.save()
    except:
        abort(500)
    return todo.to_dict(), 201


@api.route("/todolist/<int:todolist_id>/", methods=["PUT"])
def change_todolist_title(todolist_id):
    todolist = TodoList.query.get_or_404(todolist_id)
    try:
        todolist.title = request.json.get("title")
        todolist.save()
    except:
        abort(500)
    return todolist.to_dict(), 201


@api.route("/todolist/<int:todolist_id>/", methods=["DELETE"])
def delete_todolist(todolist_id):
    todolist = TodoList.query.get_or_404(todolist_id)
    try:
        if todolist_id == request.json.get("todolist_id"):
            todolist.delete()
            return todolist.to_dict(), 201
        else:
            abort(500)
    except:
        abort(500)


@api.route("/todolist/<int:todolist_id>/task/<int:task_id>/", methods=["DELETE"])
def delete_task(todolist_id, task_id):
    todo = TodoTask.query.get_or_404(task_id)
    try:
        if task_id == request.json.get("task_id"):
            todo.delete()
            return todo.to_dict(), 201
        else:
            abort(500)
    except:
        abort(500)