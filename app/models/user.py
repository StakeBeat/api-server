from sqlalchemy import Column, String, Integer, Boolean

from app.models.base import BaseModel


class User(BaseModel):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    username = Column(String(123), unique=True, nullable=False)
    password = Column(String(123), nullable=False)
    expo_token = Column(String(123), nullable=True)
    notification_enabled = Column(Boolean, nullable=True)
