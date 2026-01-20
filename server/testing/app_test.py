import pytest
from app import app, db, Episode, Guest, Appearance

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

def test_get_episodes(client):
    with app.app_context():
        episode1 = Episode(date="1/11/99", number=1)
        episode2 = Episode(date="1/12/99", number=2)
        db.session.add(episode1)
        db.session.add(episode2)
        db.session.commit()

    resp = client.get('/episodes')
    assert resp.status_code == 200
    data = resp.get_json()
    assert len(data) == 2
    assert data[0]['date'] == "1/11/99"
    assert data[0]['number'] == 1
    assert data[1]['date'] == "1/12/99"
    assert data[1]['number'] == 2

def test_get_episode_by_id(client):
    with app.app_context():
        episode = Episode(date="1/11/99", number=1)
        guest = Guest(name="Michael J. Fox", occupation="actor")
        db.session.add(episode)
        db.session.add(guest)
        db.session.commit()
        appearance = Appearance(rating=4, episode_id=episode.id, guest_id=guest.id)
        db.session.add(appearance)
        db.session.commit()
        episode_id = episode.id

    resp = client.get(f'/episodes/{episode_id}')
    assert resp.status_code == 200
    data = resp.get_json()
    assert data['date'] == "1/11/99"
    assert data['number'] == 1
    assert len(data['appearances']) == 1
    assert data['appearances'][0]['rating'] == 4
    assert data['appearances'][0]['guest']['name'] == "Michael J. Fox"

def test_get_episode_by_id_not_found(client):
    resp = client.get('/episodes/999')
    assert resp.status_code == 404
    data = resp.get_json()
    assert data['error'] == "Episode not found"

def test_get_guests(client):
    with app.app_context():
        guest1 = Guest(name="Michael J. Fox", occupation="actor")
        guest2 = Guest(name="Tracey Ullman", occupation="television actress")
        db.session.add(guest1)
        db.session.add(guest2)
        db.session.commit()

    resp = client.get('/guests')
    assert resp.status_code == 200
    data = resp.get_json()
    assert len(data) == 2
    assert data[0]['name'] == "Michael J. Fox"
    assert data[0]['occupation'] == "actor"
    assert data[1]['name'] == "Tracey Ullman"
    assert data[1]['occupation'] == "television actress"

def test_create_appearance(client):
    with app.app_context():
        episode = Episode(date="1/11/99", number=1)
        guest = Guest(name="Michael J. Fox", occupation="actor")
        db.session.add(episode)
        db.session.add(guest)
        db.session.commit()
        episode_id = episode.id
        guest_id = guest.id

    resp = client.post('/appearances', json={'rating': 5, 'episode_id': episode_id, 'guest_id': guest_id})
    assert resp.status_code == 201
    data = resp.get_json()
    assert data['rating'] == 5
    assert data['episode_id'] == episode_id
    assert data['guest_id'] == guest_id
    assert data['episode']['date'] == "1/11/99"
    assert data['guest']['name'] == "Michael J. Fox"

def test_create_appearance_invalid_rating(client):
    with app.app_context():
        episode = Episode(date="1/11/99", number=1)
        guest = Guest(name="Michael J. Fox", occupation="actor")
        db.session.add(episode)
        db.session.add(guest)
        db.session.commit()
        episode_id = episode.id
        guest_id = guest.id

    resp = client.post('/appearances', json={'rating': 6, 'episode_id': episode_id, 'guest_id': guest_id})
    assert resp.status_code == 400
    data = resp.get_json()
    assert "Rating must be between 1 and 5" in data['errors'][0]

def test_create_appearance_invalid_ids(client):
    resp = client.post('/appearances', json={'rating': 5, 'episode_id': 999, 'guest_id': 999})
    assert resp.status_code == 400
    data = resp.get_json()
    assert data['errors'] == ["Invalid episode_id or guest_id"]