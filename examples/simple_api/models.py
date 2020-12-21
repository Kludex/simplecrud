from sqlalchemy import Column, Integer, String

from examples.simple_api.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    email = Column(String(32), unique=True)
    age = Column(Integer, nullable=False)
    password_hash = Column(String(64), nullable=False)
