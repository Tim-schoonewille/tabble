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
    activated = db.Column(db.Boolean, default=False)
    is_admin = db.Column(db.Boolean, default=False)
    is_mod = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    last_login = db.Column(db.DateTime, onupdate=datetime.utcnow)
    date_of_birth = db.Column(db.DateTime, nullable=True)
    first_name = db.Column(db.String(500), nullable=True)
    last_name = db.Column(db.String(500), nullable=True)
    

    tabs_added = db.relationship('Tab', back_populates='user')
    favourite_tabs = db.relationship('Favourite', back_populates='user')


    def __repr__(self):
        return f'<USER: {self.user_uuid}>'


    def serialize(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns if c.name != 'password'}
    

class Tab(db.Model):
    tab_id = db.Column(db.Integer, primary_key=True)
    tab_uuid = db.Column(db.String(500))
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'))
    # artist = db.Column(db.String(500), nullable=False)
    artist_id = db.Column(db.Integer, db.ForeignKey('artist.artist_id'))
    title = db.Column(db.String(500), nullable=False)
    date_added = db.Column(db.DateTime, default=datetime.utcnow)
    last_editted = db.Column(db.DateTime, onupdate=datetime.utcnow)
    tab = db.Column(db.Text)
    link_to_tab = db.Column(db.String(500), nullable=False)

    user = db.relationship('User', back_populates='tabs_added')
    genres = db.relationship('Genre', secondary='tab_genre')
    favourited = db.relationship('Favourite', back_populates='tab')
    artist = db.relationship('Artist', back_populates='tabs')

    def __repr__(self):
        return f'<TAB: {self.artist} - {self.title}>'
    
    def serialize(self):
        object = {c.name: getattr(self, c.name) for c in self.__table__.columns}
        object.update(
            Artist = self.artist.name
        )
        return object
    
    def favourite(self, user):
        
        new_favourite = Favourite(tab_id=self.tab_id,
                                  tab_uuid=self.tab_uuid,
                                  user_id=user.user_id,
                                  )
        db.session.add(new_favourite)
        db.session.commit()
        
        return True


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

    def serialize(self):
        return {
            "id": self.favourite_id,
            "tab_id": self.tab_uuid,
            "date_added": self.date_added,
            "last_editted": self.last_editted,
            "completed": self.completed,
            "title": self.tab.title,
            "artist": self.tab.artist.name,
        }

class Genre(db.Model):
    genre_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(500))
    

    def __repr__(self):
        return f'<GENRE: {self.name}>'


class Registration(db.Model):
    reg_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'))
    completed = db.Column(db.Boolean, default=False)
    registration_string = db.Column(db.String(500))
    date_added = db.Column(db.DateTime, default=datetime.utcnow)
    date_confirmed = db.Column(db.DateTime)
    
    # TODO test this


class TokenBlocklist(db.Model):
    __tablename__ = 'token_blocklist'
    id = db.Column(db.Integer, primary_key=True)
    jti = db.Column(db.String(36), nullable=False, index=True)
    created_at = db.Column(db.DateTime, nullable=False)


class Artist(db.Model):
    artist_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(500), nullable=False)
    
    tabs = db.relationship('Tab', back_populates='artist')
    
    
    def __repr__(self):
        return f'<ARTIST: {self.name}>'
    
    
    def serialize(self):
        
        artist_tabs = [Tab.serialize(tab) for tab in self.tabs]
        
        return {
            "name": self.name,
            "tabs": artist_tabs
        }
    