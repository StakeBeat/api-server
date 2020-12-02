from typing import List
from sqlalchemy import tuple_

from app.services.user import UserService
from app.models.validator import Validator
from app.session import SessionManager


class ValidatorService:
    def __init__(self) -> None:
        self.user_svc = UserService()

    def update(self, indices: List[str], user_id: int) -> None:
        cur_validators = self.user_svc.get_all_validators(user_id)
        cur_validator_indices = [validator.indice for validator in cur_validators]
        to_delete = set(cur_validator_indices) - set(indices)
        to_add = set(indices) - set(cur_validator_indices)
        validators_to_add = [Validator(indice=i, user_id=user_id) for i in to_add]
        validators_to_del = [(i, user_id) for i in to_delete]

        with SessionManager.session() as session:
            session.query(Validator).filter(
                tuple_(Validator.indice, Validator.user_id).in_(validators_to_del)
            ).delete(synchronize_session=False)
            session.add_all(validators_to_add)
