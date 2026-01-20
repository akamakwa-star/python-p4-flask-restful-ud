import pytest
from faker import Faker
from app import app, Camper, Signup

def test_validates_camper_age():
    '''require campers to have ages between 8 and 18, inclusive.'''
    with pytest.raises(ValueError):
        Camper(name=Faker().name(), age=0)

def test_validates_camper_name():
    '''require campers to have names.'''
    with app.app_context():
        with pytest.raises(ValueError):
            Camper(name=None, age=10)

def test_validates_signup_time():
    '''requires signups to have integer times between 0 and 23, inclusive.'''
    with pytest.raises(ValueError):
        Signup(time=-1, camper_id=1, activity_id=1)