from sqlalchemy import Column, String, Integer

from app.models.base import BaseModel


class User(BaseModel):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    username = Column(String(123), unique=True, nullable=False)
    email = Column(String(123), unique=True, nullable=False)
    password = Column(String(123), nullable=False)
