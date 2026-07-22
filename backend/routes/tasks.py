from flask_restful import Resource, request
from extensions import db
from models import Task

class TaskResource(Resource):
    def get(self):
        tasks = Task.query.all()
        data = []
        for task in tasks:
            data.append({'id':task.id, 'title':task.title})
        return {'msg': data}
    
    def post(self):
        data = request.get_json()
        title = data.get('title')
        description = data.get('description')

        task = Task(title=title, description=description)
        db.session.add(task)
        db.session.commit()
        return {'msg': 'task created', 'task': {'id': task.id, 'title': task.title, 'description': task.description}}
    
    def put(self, id):
        data = request.get_json()

        task = Task.query.get(id)
        
        task.title = data.get('title')
        task.description = data.get('description')
        db.session.commit()
        return {'msg': 'task updated'}
    
    def delete(self, id):
        task = Task.query.get(id)
        db.session.delete(task)
        db.session.commit()
        return {'msg': 'delete'}