from app import db
from app import login
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    # dynamic relationships here make our life easy as they return
    # SQLAlchemy objects for relational queries
    artist_reviews = db.relationship('ArtistReview', backref='author', lazy='dynamic')
    album_reviews = db.relationship('AlbumReview', backref='author', lazy='dynamic')
    song_reviews = db.relationship('SongReview', backref='author', lazy='dynamic')

    def __repr__(self):
        return f"<User {self.username} | Email: {self.email}>"

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class ArtistReview(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    artist_id = db.Column(db.String(120), index=True)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    content = db.Column(db.String(20000), index=True)
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return f"<Post about artist {self.artist_id} | Made By: {self.author.username} | " \
               f"Content: {self.content}>"


class AlbumReview(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    album_id = db.Column(db.String(120), index=True)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    content = db.Column(db.String(20000), index=True)
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    artist_id = db.Column(db.String(120), index=True)

    def __repr__(self):
        return f"<Post about album {self.album_id} by {self.artist_id} | " \
               f"Made By: {self.author} |" \
               f"Content: {self.content}>"


class SongReview(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    song_id = db.Column(db.String(120), index=True)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    content = db.Column(db.String(20000), index=True)
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    album_id = db.Column(db.String(120), index=True)
    artist_id = db.Column(db.String(120), index=True)

    def __repr__(self):
        return f"<Post about song {self.song_id} by {self.artist_id} in {self.album_id} | " \
               f"Made By: {self.author} | " \
               f"Content: {self.content}>"


@login.user_loader
def load_user(id):
    return db.session.get(User, int(id))
