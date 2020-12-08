from dataclasses import dataclass

from app.models.validator import Validator


@dataclass
class ValidatorDT:
    id: int
    indice: str
    pubkey: str
    user_id: int

    @classmethod
    def from_model(cls, model: Validator) -> 'ValidatorDT':
        return cls(
            id=model.id,
            indice=model.indice,
            pubkey=model.pubkey[:10] if model.pubkey else '',
            user_id=model.user_id,
        )
