from typing import Any, Dict


class Borg(object):
    __shared_state: Dict[Any, Any] = {}

    def __new__(cls) -> 'Borg':
        instance = super().__new__(cls)
        instance.__dict__ = cls.__shared_state
        return instance

    def __init__(self) -> None:
        pass
