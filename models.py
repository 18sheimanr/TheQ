from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from app import db


class Host(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), nullable=False,
                         unique=True, index=True)
    password_hash = db.Column(db.String(128))

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @property
    def token_expired(self):
        return False

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return '<Host username %r>' % self.username


class Event(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), nullable=False, unique=True)
    songs = db.relationship("Song", backref="event")

    def __repr__(self):
        return '<Event %r>' % self.id


class Song(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), nullable=False)
    artist = db.Column(db.String(64), nullable=False)
    rating = db.Column(db.SmallInteger, nullable=False)
    event_id = db.Column(db.Integer, db.ForeignKey('event.id'))