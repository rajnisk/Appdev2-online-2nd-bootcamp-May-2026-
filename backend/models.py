from datetime import datetime
from extensions import db


class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=True)
    # completed = db.Column(db.Boolean, default=False)
    # created_at = db.Column(db.DateTime, default=datetime.utcnow)
