#!/usr/bin/env python3

from flask import Flask, request, make_response, jsonify
from flask_migrate import Migrate
from flask_restful import Api, Resource
from sqlalchemy.exc import IntegrityError

from models import db, Episode, Guest, Appearance

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)
db.init_app(app)

api = Api(app)

class Episodes(Resource):
    def get(self):
        episodes = [episode.to_dict() for episode in Episode.query.all()]
        return make_response(episodes, 200)

class EpisodeById(Resource):
    def get(self, id):
        episode = Episode.query.filter_by(id=id).first()
        if not episode:
            return make_response({"error": "Episode not found"}, 404)
        episode_dict = episode.to_dict()
        episode_dict['appearances'] = [appearance.to_dict() for appearance in episode.appearances]
        return make_response(episode_dict, 200)

class Guests(Resource):
    def get(self):
        guests = [guest.to_dict() for guest in Guest.query.all()]
        return make_response(guests, 200)

class Appearances(Resource):
    def post(self):
        data = request.get_json()
        try:
            appearance = Appearance(
                rating=data['rating'],
                episode_id=data['episode_id'],
                guest_id=data['guest_id']
            )
            db.session.add(appearance)
            db.session.commit()
            appearance_dict = appearance.to_dict()
            appearance_dict['episode'] = appearance.episode.to_dict()
            appearance_dict['guest'] = appearance.guest.to_dict()
            return make_response(appearance_dict, 201)
        except ValueError as e:
            return make_response({"errors": [str(e)]}, 400)
        except IntegrityError:
            return make_response({"errors": ["Invalid episode_id or guest_id"]}, 400)

api.add_resource(Episodes, '/episodes')
api.add_resource(EpisodeById, '/episodes/<int:id>')
api.add_resource(Guests, '/guests')
api.add_resource(Appearances, '/appearances')

if __name__ == '__main__':
    app.run(port=5555, debug=True)