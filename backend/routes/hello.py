from flask_restful import Resource, request


class HelloWorld(Resource):
    def get(self):
        return {'student_data': [{'name': 'Joe', 'age': 20}, {'name': 'Jane', 'age': 21}, {'name': 'John', 'age': 22}]}
    
    def post(self):
        data = request.get_json()
        print(data)
        return {'msg': 'post'}
    
    def put(self):
        return {'msg': 'put'}