from datetime import datetime


from flask import Flask
from flask_restful import Resource, Api
from extensions import db
from models import Task
from flask_cors import CORS

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///project.db"


api = Api(app)
db.init_app(app)
CORS(app)

with app.app_context():
    # db.drop_all()
    db.create_all()
    



# @app.route("/", methods=['post'])
# def hello_world():
#     return "<p>Hello, World!</p>"

# @app.route("/help")
# def help_world():
#     return "<p>help!</p>"


# from routes.hello import HelloWorld
# api.add_resource(HelloWorld, '/')
from routes import register_routes

register_routes(api)

app.run(debug=True)