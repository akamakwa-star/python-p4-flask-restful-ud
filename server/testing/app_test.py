import pytest
from faker import Faker
from random import randint
from app import app, db, Camper, Activity, Signup

@pytest.fixture
def client():
    with app.test_client() as client:
        with app.app_context():
            db.create_all()
            db.session.execute(db.text("PRAGMA foreign_keys = ON"))
            db.session.commit()
        yield client
        with app.app_context():
            db.drop_all()

def test_gets_campers(client):
    '''retrieves campers with GET requests to /campers.'''
    with app.app_context():
        camper1 = Camper(name=Faker().name(), age=9)
        camper2 = Camper(name=Faker().name(), age=12)
        db.session.add_all([camper1, camper2])
        db.session.commit()

    response = client.get('/campers')
    assert response.status_code == 200
    data = response.get_json()
    assert len(data) == 2

def test_returns_404_if_no_camper(client):
    '''returns an error message and 404 status code when a camper is searched by a non-existent ID.'''
    response = client.get('/campers/0')
    assert response.status_code == 404
    assert response.get_json().get('error') == "Camper not found"

def test_creates_camper(client):
    '''creates one camper using a name and age with a POST request to /campers.'''
    name = Faker().name()
    age = randint(8, 18)
    response = client.post(
        '/campers',
        json={
            'name': name,
            'age': age
        }
    )
    assert response.status_code == 201
    data = response.get_json()
    assert data['id']
    assert data['name'] == name
    assert data['age'] == age

def test_400_for_camper_validation_error(client):
    '''returns a 400 status code and error message if a POST request to /campers fails.'''
    response = client.post(
        '/campers',
        json={
            'name': Faker().name(),
            'age': 19
        }
    )
    assert response.status_code == 400
    data = response.get_json()
    assert 'errors' in data

def test_gets_camper_by_id(client):
    '''retrieves one camper using its ID with GET request to /campers/<int:id>.'''
    with app.app_context():
        fake = Faker()
        camper = Camper(name=fake.name(), age=11)
        activity = Activity(name=fake.sentence(), difficulty=4)
        db.session.add_all([camper, activity])
        db.session.commit()
        signup = Signup(time=10, camper_id=camper.id, activity_id=activity.id)
        db.session.add(signup)
        db.session.commit()
        camper_id = camper.id
        camper_name = camper.name
        camper_age = camper.age
        activity_name = activity.name

    response = client.get(f'/campers/{camper_id}')
    assert response.status_code == 200
    data = response.get_json()
    assert data['name'] == camper_name
    assert data['age'] == camper_age
    assert len(data['activities']) == 1
    assert data['activities'][0]['name'] == activity_name

def test_patch_campers_by_id(client):
    '''updates campers with PATCH request to /campers/<int:id>.'''
    with app.app_context():
        camper = Camper(name=Faker().name(), age=10)
        db.session.add(camper)
        db.session.commit()

        new_name = Faker().name()
        response = client.patch(
            f'/campers/{camper.id}',
            json={
                'name': new_name,
                'age': 11
            }
        )
        assert response.status_code == 200
        data = response.get_json()
        assert data['name'] == new_name
        assert data['age'] == 11

def test_validates_camper_update(client):
    '''returns an error message if a PATCH request to /campers/<int:id> is invalid.'''
    with app.app_context():
        fake = Faker()
        camper = Camper(name=fake.name(), age=10)
        db.session.add(camper)
        db.session.commit()

        response = client.patch(
            f'/campers/{camper.id}',
            json={
                'age': 7
            }
        )
        assert response.status_code == 400
        data = response.get_json()
        assert 'errors' in data

def test_404_no_activity_to_patch(client):
    '''returns an error message if a PATCH request to /campers/<int:id> references a non-existent camper'''
    response = client.patch(
        f'/campers/0',
        json={
            'name': 'some name',
            'age': 9
        })
    assert response.status_code == 404
    assert response.content_type == 'application/json'
    data = response.get_json()
    assert data['error'] == "Camper not found"

def test_deletes_activities_by_id(client):
    '''deletes activities with DELETE request to /activities/<int:id>.'''
    with app.app_context():
        activity = Activity(name=Faker().sentence(), difficulty=randint(1, 10))
        db.session.add(activity)
        db.session.commit()

        response = client.delete(f'/activities/{activity.id}')
        assert response.status_code == 204

        # Check deleted
        response2 = client.get(f'/activities/{activity.id}')
        assert response2.status_code == 404

def test_gets_activities(client):
    '''retrieves activities with GET request to /activities'''
    with app.app_context():
        fake = Faker()
        activity1 = Activity(
            name=fake.sentence(), difficulty=randint(1, 10))
        activity2 = Activity(
            name=fake.sentence(), difficulty=randint(1, 10))
        db.session.add_all([activity1, activity2])
        db.session.commit()

    response = client.get('/activities')
    assert response.status_code == 200
    data = response.get_json()
    assert len(data) == 2

def test_returns_404_if_no_activity(client):
    '''returns 404 status code with DELETE request to /activities/<int:id> if activity does not exist.'''
    response = client.delete('/activities/0')
    assert response.status_code == 404
    assert response.get_json().get('error') == 'Activity not found'

def test_creates_signups(client):
    '''creates signups with POST request to /signups'''
    with app.app_context():
        fake = Faker()
        camper = Camper(name=fake.name(), age=randint(8, 18))
        activity = Activity(name=fake.sentence(), difficulty=randint(1, 10))
        db.session.add_all([camper, activity])
        db.session.commit()

        response = client.post(
            '/signups',
            json={
                'time': 10,
                'camper_id': camper.id,
                'activity_id': activity.id
            }
        )
        assert response.status_code == 201
        data = response.get_json()
        assert data['time'] == 10
        assert data['camper']['name'] == camper.name
        assert data['activity']['name'] == activity.name

def test_400_for_signup_validation_error(client):
    '''returns a 400 status code and error message if a POST request to /signups fails.'''
    with app.app_context():
        fake = Faker()
        camper = Camper(name=fake.name(), age=randint(8, 18))
        activity = Activity(name=fake.sentence(), difficulty=randint(1, 10))
        db.session.add_all([camper, activity])
        db.session.commit()

        response = client.post(
            '/signups',
            json={
                'time': 25,
                'camper_id': camper.id,
                'activity_id': activity.id
            }
        )
        assert response.status_code == 400
        data = response.get_json()
        assert 'errors' in data