from routes.hello import HelloWorld
from routes.tasks import TaskResource

def register_routes(api):
    api.add_resource(HelloWorld, '/')
    api.add_resource(TaskResource, '/tasks', '/task/<int:id>')