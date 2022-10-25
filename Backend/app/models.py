from uuid import uuid4
from app.ext import db
from datetime import datetime



tab_genre = db.Table('tab_genre', 
                    db.Column('tab_id', db.Integer, db.ForeignKey('tab.tab_id')),
                    db.Column('genre_id', db.Integer, db.ForeignKey('genre.genre_id')))


class User(db.Model):
    user_id = db.Column(db.Integer, primary_key=True)
    user_uuid = db.Column(db.String(500))
    email = db.Column(db.String(500), unique=True, nullable=False)
    password = db.Column(db.String(500), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)
    is_mod = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    last_login = db.Column(db.DateTime, onupdate=datetime.utcnow)
    date_of_birth = db.Column(db.DateTime, nullable=True)
    first_name = db.Column(db.String(500), nullable=True)
    last_name = db.Column(db.String(500), nullable=True)
    # TODO Add something so user has to activate.

    tabs_added = db.relationship('Tab', back_populates='user')
    favourite_tabs = db.relationship('Favourite', back_populates='user')


    def __repr__(self):
        return f'<USER: {self.user_uuid}>'


class Tab(db.Model):
    tab_id = db.Column(db.Integer, primary_key=True)
    tab_uuid = db.Column(db.String(500))
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'))
    artist = db.Column(db.String(500), nullable=False)
    title = db.Column(db.String(500), nullable=False)
    date_added = db.Column(db.DateTime, default=datetime.utcnow)
    last_editted = db.Column(db.DateTime, onupdate=datetime.utcnow)
    tab = db.Column(db.Text)
    link_to_tab = db.Column(db.String(500), nullable=False)

    user = db.relationship('User', back_populates='tabs_added')
    genres = db.relationship('Genre', secondary='tab_genre')
    favourited = db.relationship('Favourite', back_populates='tab')

    def __repr__(self):
        return f'<TAB: {self.artist} - {self.title}>'


class Favourite(db.Model):
    favourite_id = db.Column(db.Integer, primary_key=True)
    tab_id = db.Column(db.Integer, db.ForeignKey('tab.tab_id'))
    tab_uuid = db.Column(db.String(500))
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'))
    date_added = db.Column(db.DateTime, default=datetime.utcnow)
    last_editted = db.Column(db.DateTime, onupdate=datetime.utcnow)
    completed = db.Column(db.Boolean, default=False)

    user = db.relationship('User', back_populates='favourite_tabs')
    tab = db.relationship('Tab', back_populates='favourited')



class Genre(db.Model):
    genre_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(500))
    

    def __repr__(self):
        return f'<GENRE: {self.name}>'

