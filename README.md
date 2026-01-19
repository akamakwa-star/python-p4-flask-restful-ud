 Late Show API

 Project Description

The Late Show API is a Flask-based RESTful API that models episodes of a late-night show, the guests who appear on those episodes, and their appearances. The API allows users to retrieve episodes and guests, as well as create new appearances with validations.

This project was built as part of Phase 4 Code Challenge at Moringa School.

🛠️ Technologies Used

Python

Flask

Flask SQLAlchemy

Flask Migrate

SQLite / PostgreSQL

SQLAlchemy Serializer

Postman (for API testing)

Database Models
Episode

id (Integer, Primary Key)

date (String)

number (Integer)

Relationships:

Has many guests through appearances

Cascade delete enabled

Guest

id (Integer, Primary Key)

name (String)

occupation (String)

Relationships:

Has many episodes through appearances

Cascade delete enabled

Appearance

id (Integer, Primary Key)

rating (Integer)

episode_id (Foreign Key)

guest_id (Foreign Key)

Validations:

rating must be between 1 and 5 (inclusive)

🔗 Relationships

An Episode has many Guests through Appearances

A Guest has many Episodes through Appearances

An Appearance belongs to both a Guest and an Episode

Setup Instructions
1. Clone the repository
git clone git@github.com:your-username/lateshow-firstname-lastname.git
cd lateshow-firstname-lastname

2. Create and activate a virtual environment
pipenv install
pipenv shell

3. Install dependencies
pip install -r requirements.txt

4. Run database migrations
flask db init
flask db migrate
flask db upgrade

5. Seed the database
python seed.py

6. Start the server
flask run

 API Endpoints
GET /episodes

Returns a list of all episodes.

[
  {
    "id": 1,
    "date": "1/11/99",
    "number": 1
  }
]

GET /episodes/:id

Returns a single episode and its appearances.

Success Response

{
  "id": 1,
  "date": "1/11/99",
  "number": 1,
  "appearances": [
    {
      "id": 1,
      "rating": 4,
      "episode_id": 1,
      "guest_id": 1,
      "guest": {
        "id": 1,
        "name": "Michael J. Fox",
        "occupation": "actor"
      }
    }
  ]
}


Error Response

{
  "error": "Episode not found"
}

GET /guests

Returns all guests.

[
  {
    "id": 1,
    "name": "Michael J. Fox",
    "occupation": "actor"
  }
]

POST /appearances

Creates a new appearance.

Request Body

{
  "rating": 5,
  "episode_id": 2,
  "guest_id": 3
}


Success Response

{
  "id": 162,
  "rating": 5,
  "episode_id": 2,
  "guest_id": 3,
  "episode": {
    "id": 2,
    "date": "1/12/99",
    "number": 2
  },
  "guest": {
    "id": 3,
    "name": "Tracey Ullman",
    "occupation": "television actress"
  }
}


Error Response

{
  "errors": ["validation errors"]
}

 Validations

Appearance rating must be between 1 and 5

Invalid submissions return error messages with appropriate HTTP status codes

 Testing

Import the provided Postman collection

Test all routes to ensure expected responses

All endpoints return JSON responses