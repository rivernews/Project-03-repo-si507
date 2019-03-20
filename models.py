from sqlalchemy import func
from server import db, session

import uuid

def generate_uuid(prefix = ""):
    def prefixed_uuid(prefix):
        return f"{prefix}-{uuid.uuid4()}"
    return prefixed_uuid

class Base(db.Model):
    __abstract__ = True

    def save(self):
        session.add(self)
        try:
            session.commit()
        except:
            session.rollback()
            raise
        return self

class Movie(Base):
    __tablename__ = "movies"
    id = db.Column(db.String(64), primary_key=True, default=generate_uuid("movie"), nullable=False)
    name = db.Column(db.String(64))
    
    major_genre_id = db.Column(db.String(64), db.ForeignKey("genres.id"), nullable=True)
    major_genre = db.relationship('Genre', backref='Movie')

    def __str__(self):
        return f"{self.name} ({self.major_genre.name})"
    
    @staticmethod
    def count():
        return session.query(func.count(Movie.id))
    
    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'major_genre': self.major_genre.name,
        }
    
    @property
    def get_json_url(self):
        return f"/movies/{self.id}/"


class Genre(Base):
    __tablename__ = "genres"
    id = db.Column(db.String(64), primary_key=True, default=generate_uuid("genre"), nullable=False)
    name = db.Column(db.String(64))

    def __str__(self):
        return f"{self.name}"
        
    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
        }
    
    @property
    def get_json_url(self):
        return f"/genres/{self.id}/"