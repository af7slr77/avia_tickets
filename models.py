from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
import secrets
import uuid

Base = SQLAlchemy()
bcrypt = Bcrypt()

class User(Base.Model):
    id = Base.Column(Base.String(36), primary_key=True, default=str(uuid.uuid4()))
    username = Base.Column(Base.String(80), unique=True, nullable=False)
    password = Base.Column(Base.String(120), nullable=False)
    salt = Base.Column(Base.String(29), nullable=False)

    def __repr__(self):
        return f'{self.username}'
