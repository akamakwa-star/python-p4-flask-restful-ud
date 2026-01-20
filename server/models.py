from flask_sqlalchemy import SQLAlchemy
from sqlalchemy_serializer import SerializerMixin

db = SQLAlchemy()

class Camper(db.Model, SerializerMixin):
    __tablename__ = 'campers'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    age = db.Column(db.Integer)

    signups = db.relationship('Signup', backref='camper', cascade='all, delete-orphan')

    serialize_rules = ('-signups.camper',)

    def __init__(self, name, age):
        if not name:
            raise ValueError("Name cannot be empty")
        if not (8 <= age <= 18):
            raise ValueError("Age must be between 8 and 18")
        self.name = name
        self.age = age

    def __repr__(self):
        return f'<Camper {self.name}, age {self.age}.>'

class Activity(db.Model, SerializerMixin):
    __tablename__ = 'activities'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    difficulty = db.Column(db.Integer)

    signups = db.relationship('Signup', backref='activity', cascade='all, delete-orphan')

    serialize_rules = ('-signups.activity',)

    def __repr__(self):
        return f'<Activity {self.name}, difficulty {self.difficulty}.>'

class Signup(db.Model, SerializerMixin):
    __tablename__ = 'signups'

    id = db.Column(db.Integer, primary_key=True)
    time = db.Column(db.Integer)
    camper_id = db.Column(db.Integer, db.ForeignKey('campers.id'))
    activity_id = db.Column(db.Integer, db.ForeignKey('activities.id'))

    serialize_rules = ('-camper.signups', '-activity.signups')

    def __init__(self, time, camper_id, activity_id):
        if not (0 <= time <= 23):
            raise ValueError("Time must be between 0 and 23")
        self.time = time
        self.camper_id = camper_id
        self.activity_id = activity_id

    def __repr__(self):
        return f'<Signup time {self.time}, camper {self.camper_id}, activity {self.activity_id}.>'
        return rating
