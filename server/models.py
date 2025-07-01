from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from sqlalchemy_serializer import SerializerMixin
from datetime import datetime
from sqlalchemy.orm import validates


metadata = MetaData(naming_convention={
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
})

db = SQLAlchemy(metadata=metadata)

class Message(db.Model, SerializerMixin):
    __tablename__ = 'messages'

    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String, nullable=False)
    username = db.Column(db.String, nullable=False)
    created_at = db.Column(db.DateTime(), default=datetime.now)
    updated_at = db.Column(db.DateTime(), onupdate=datetime.now)

    serialize_rules = ('created_at', 'updated_at')

    def __repr__(self):
        return f'<Messagee {self.id}: {self.username} - {self.body[:20]}...>'
    
    @validates("body")
    def validate_body(self, key, body):
        if not isinstance(body, str) or len(body.strip()) == 0:
            raise ValueError("Message body must be a non-empty string.")
        return body
    

    @validates('username')
    def validate_username(self, key, username):
        if not isinstance(username, str) or len(username.strip()) == 0:
            raise ValueError("Username must be a non-empty string.")
        return username