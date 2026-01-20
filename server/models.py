from flask_sqlalchemy import SQLAlchemy
from sqlalchemy_serializer import SerializerMixin

db = SQLAlchemy()

class Episode(db.Model, SerializerMixin):
    __tablename__ = 'episodes'

    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.String)
    number = db.Column(db.Integer)

    appearances = db.relationship('Appearance', backref='episode', cascade='all, delete-orphan')

    serialize_rules = ('-appearances.episode',)

    def __repr__(self):
        return f'<Episode {self.number}, date {self.date}.>'

class Guest(db.Model, SerializerMixin):
    __tablename__ = 'guests'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    occupation = db.Column(db.String)

    appearances = db.relationship('Appearance', backref='guest', cascade='all, delete-orphan')

    serialize_rules = ('-appearances.guest',)

    def __repr__(self):
        return f'<Guest {self.name}, occupation {self.occupation}.>'

class Appearance(db.Model, SerializerMixin):
    __tablename__ = 'appearances'

    id = db.Column(db.Integer, primary_key=True)
    rating = db.Column(db.Integer)
    episode_id = db.Column(db.Integer, db.ForeignKey('episodes.id'))
    guest_id = db.Column(db.Integer, db.ForeignKey('guests.id'))

    serialize_rules = ('-episode.appearances', '-guest.appearances')

    def __repr__(self):
        return f'<Appearance rating {self.rating}, episode {self.episode_id}, guest {self.guest_id}.>'

    @db.validates('rating')
    def validate_rating(self, key, rating):
        if not (1 <= rating <= 5):
            raise ValueError("Rating must be between 1 and 5")
        return rating
