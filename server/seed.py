#!/usr/bin/env python3

from faker import Faker
import random

from app import app
from models import db, Episode, Guest, Appearance

with app.app_context():
    
    fake = Faker()

    # Clear existing data
    Appearance.query.delete()
    Guest.query.delete()
    Episode.query.delete()

    # Create episodes
    episodes = []
    for i in range(10):
        episode = Episode(
            date=fake.date(),
            number=i+1
        )
        episodes.append(episode)

    db.session.add_all(episodes)
    db.session.commit()

    # Create guests
    guests = []
    for i in range(20):
        guest = Guest(
            name=fake.name(),
            occupation=fake.job()
        )
        guests.append(guest)

    db.session.add_all(guests)
    db.session.commit()

    # Create appearances
    appearances = []
    for i in range(50):
        appearance = Appearance(
            rating=random.randint(1, 5),
            episode_id=random.choice(episodes).id,
            guest_id=random.choice(guests).id
        )
        appearances.append(appearance)

    db.session.add_all(appearances)
    db.session.commit()
