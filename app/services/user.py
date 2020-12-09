from typing import Dict, List
import bcrypt

from app.session import SessionManager
from app.models.user import User
from app.models.validator import Validator


class UserService:
    def __init__(self) -> None:
        pass

    def create(self, payload: Dict[str, str]) -> User:
        hashed_pw = bcrypt.hashpw(payload['password'].encode(), bcrypt.gensalt())
        user = User(username=payload['username'], password=hashed_pw.decode())

        with SessionManager.session() as session:
            session.add(user)

        return user

    def get_all_validators(self, user_id: int) -> List[Validator]:
        with SessionManager.session() as session:
            validators = session.query(Validator).filter_by(user_id=user_id)

        return validators

    def update(self, user_id: int, payload: Dict[str, str]) -> None:
        with SessionManager.session() as session:
            user = session.query(User).get(user_id)
            user.expo_token = payload['expoToken']
            user.notification_enabled = payload['notificationEnabled']
