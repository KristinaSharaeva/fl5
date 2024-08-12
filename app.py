from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from pydantic import ValidationError
from models import db, Task
from schemas import TaskCreate, TaskUpdate

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tasks.db'
db.init_app(app)

@app.before_first_request
def create_tables():
    db.create_all()

@app.route('/tasks', methods=['GET'])
def get_tasks():
    tasks = Task.query.all()
    return jsonify([{"id": task.id, "title": task.title, "description": task.description, "is_completed": task.is_completed} for task in tasks])

@app.route('/tasks/<int:id>', methods=['GET'])
def get_task(id):
    task = Task.query.get_or_404(id)
    return jsonify({"id": task.id, "title": task.title, "description": task.description, "is_completed": task.is_completed})

@app.route('/tasks', methods=['POST'])
def create_task():
    try:
        task_data = TaskCreate(**request.json)
    except ValidationError as e:
        return jsonify(e.errors()), 400

    new_task = Task(title=task_data.title, description=task_data.description, is_completed=task_data.is_completed)
    db.session.add(new_task)
    db.session.commit()
    return jsonify({"id": new_task.id, "title": new_task.title, "description": new_task.description, "is_completed": new_task.is_completed}), 201

@app.route('/tasks/<int:id>', methods=['PUT'])
def update_task(id):
    task = Task.query.get_or_404(id)
    try:
        task_data = TaskUpdate(**request.json)
    except ValidationError as e:
        return jsonify(e.errors()), 400

    if task_data.title:
        task.title = task_data.title
    if task_data.description:
        task.description = task_data.description
    if task_data.is_completed is not None:
        task.is_completed = task_data.is_completed

    db.session.commit()
    return jsonify({"id": task.id, "title": task.title, "description": task.description, "is_completed": task.is_completed})

@app.route('/tasks/<int:id>', methods=['DELETE'])
def delete_task(id):
    task = Task.query.get_or_404(id)
    db.session.delete(task)
    db.session.commit()
    return '', 204

if __name__ == '__main__':
    app.run(debug=True)
