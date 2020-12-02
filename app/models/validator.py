from sqlalchemy import Column, String, Integer, ForeignKey

from app.models.base import BaseModel
from app.models.user import User


class Validator(BaseModel):
    __tablename__ = "validators"

    id = Column(Integer, primary_key=True)
    indice = Column(String(16), nullable=False, index=True)
    user_id = Column(Integer, ForeignKey(User.id), index=True)
