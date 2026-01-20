#!/usr/bin/env python3

from flask import Flask, request, make_response, jsonify
from flask_migrate import Migrate
from flask_restful import Api, Resource
from sqlalchemy.exc import IntegrityError

from models import db, Camper, Activity, Signup

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)
db.init_app(app)

api = Api(app)

class Campers(Resource):
    def get(self):
        campers = [camper.to_dict() for camper in Camper.query.all()]
        return make_response(campers, 200)

    def post(self):
        data = request.get_json()
        try:
            camper = Camper(
                name=data['name'],
                age=data['age']
            )
            db.session.add(camper)
            db.session.commit()
            return make_response(camper.to_dict(), 201)
        except ValueError as e:
            return make_response({"errors": [str(e)]}, 400)

class CamperById(Resource):
    def get(self, id):
        camper = Camper.query.filter_by(id=id).first()
        if not camper:
            return make_response({"error": "Camper not found"}, 404)
        camper_dict = camper.to_dict()
        camper_dict['activities'] = [signup.activity.to_dict() for signup in camper.signups]
        return make_response(camper_dict, 200)

    def patch(self, id):
        camper = Camper.query.filter_by(id=id).first()
        if not camper:
            return make_response({"error": "Camper not found"}, 404)
        data = request.get_json()
        try:
            if 'name' in data:
                camper.name = data['name']
            if 'age' in data:
                camper.age = data['age']
            # Validate
            if not camper.name:
                raise ValueError("Name cannot be empty")
            if not (8 <= camper.age <= 18):
                raise ValueError("Age must be between 8 and 18")
            db.session.commit()
            return make_response(camper.to_dict(), 200)
        except ValueError as e:
            return make_response({"errors": [str(e)]}, 400)

    def delete(self, id):
        camper = Camper.query.filter_by(id=id).first()
        if not camper:
            return make_response({"error": "Camper not found"}, 404)
        db.session.delete(camper)
        db.session.commit()
        return make_response({}, 204)

class Activities(Resource):
    def get(self):
        activities = [activity.to_dict() for activity in Activity.query.all()]
        return make_response(activities, 200)

    def post(self):
        data = request.get_json()
        try:
            activity = Activity(
                name=data['name'],
                difficulty=data['difficulty']
            )
            db.session.add(activity)
            db.session.commit()
            return make_response(activity.to_dict(), 201)
        except ValueError as e:
            return make_response({"errors": [str(e)]}, 400)

class ActivityById(Resource):
    def get(self, id):
        activity = Activity.query.filter_by(id=id).first()
        if not activity:
            return make_response({"error": "Activity not found"}, 404)
        activity_dict = activity.to_dict()
        activity_dict['signups'] = [signup.to_dict() for signup in activity.signups]
        return make_response(activity_dict, 200)

    def delete(self, id):
        activity = Activity.query.filter_by(id=id).first()
        if not activity:
            return make_response({"error": "Activity not found"}, 404)
        db.session.delete(activity)
        db.session.commit()
        return make_response({}, 204)

class Signups(Resource):
    def post(self):
        data = request.get_json()
        try:
            signup = Signup(
                time=data['time'],
                camper_id=data['camper_id'],
                activity_id=data['activity_id']
            )
            db.session.add(signup)
            db.session.commit()
            signup_dict = signup.to_dict()
            signup_dict['camper'] = signup.camper.to_dict()
            signup_dict['activity'] = signup.activity.to_dict()
            return make_response(signup_dict, 201)
        except ValueError as e:
            return make_response({"errors": [str(e)]}, 400)
        except IntegrityError:
            return make_response({"errors": ["Invalid camper_id or activity_id"]}, 400)

api.add_resource(Campers, '/campers')
api.add_resource(CamperById, '/campers/<int:id>')
api.add_resource(Activities, '/activities')
api.add_resource(ActivityById, '/activities/<int:id>')
api.add_resource(Signups, '/signups')

if __name__ == '__main__':
    app.run(port=5555, debug=True)