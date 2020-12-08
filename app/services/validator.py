import requests
import time
from typing import Dict, List, Tuple

from app.services.user import UserService
from app.models.validator import Validator
from app.session import SessionManager
from app.dataclasses.validator import ValidatorDT
from app.utils.conversion import b64_to_hex

from app import config


class ValidatorService:
    def __init__(self, user_id: int) -> None:
        self.user_svc = UserService()
        self.user_id = user_id
        cur_validators = self.user_svc.get_all_validators(user_id)
        self.indices = [validator.indice for validator in cur_validators]

    def create(self, indices: List[str]) -> List[ValidatorDT]:
        resp = requests.get(f'{config.BEACON_RPC_URI}/validators', params={'indices': indices})
        resp = resp.json()
        index_to_pubkey = {}
        for val in resp['validatorList']:
            index_to_pubkey[val['index']] = b64_to_hex(val['validator']['publicKey'])
        validators_to_add = [
            Validator(indice=i, pubkey=index_to_pubkey[i], user_id=self.user_id) for i in indices
        ]
        with SessionManager.session() as session:
            session.add_all(validators_to_add)

        return [ValidatorDT.from_model(m) for m in validators_to_add]

    def remove(self, indice: str) -> None:
        with SessionManager.session() as session:
            session.query(Validator).filter_by(indice=indice, user_id=self.user_id).delete(
                synchronize_session=False
            )

    def get(self) -> List[ValidatorDT]:
        with SessionManager.session() as session:
            rows = session.query(Validator).filter_by(user_id=self.user_id).all()

        return [ValidatorDT.from_model(m) for m in rows]

    def info(self) -> Dict:
        """Retrieve a validator total balance, balance over time,
        avg rating and rating per index.
        """
        activation_epoch = self._get_activation_epoch()
        balances = self._get_balance(activation_epoch)
        validator_perf = self._get_validator_performance(activation_epoch)
        return {
            'balances': balances,
            'perf': validator_perf,
            'activation_epoch': activation_epoch,
        }

    def _get_validator_performance(self, activation_epoch: Dict[str, str]) -> Dict:
        """GET eth/v1alpha1/validators/performance
        Retrieve the inclusion distance for each validators assigned to current_user
        """

        def rate_inclusion_dist(distance: int) -> str:
            if distance == 0:
                return '?'
            if distance == 1:
                return 'A'
            if distance >= 2 and distance <= 3:
                return 'B'
            if distance >= 4 and distance <= 8:
                return 'C'
            if distance >= 9 and distance <= 12:
                return 'D'
            if distance >= 13:
                return 'F'

        cur_epoch = int(self._get_current_epoch())
        filter_active_indices = [
            i for i in self.indices if int(activation_epoch[i]) <= int(cur_epoch)
        ]
        if len(filter_active_indices) == 0:
            return {i: '?' for i in self.indices}
        resp = requests.get(
            f'{config.BEACON_RPC_URI}/validators/performance', params={'indices': self.indices}
        )
        resp = resp.json()
        validator_perf = {i: '?' for i in self.indices}
        sum_distance = 0
        for n, inclusion_dist in enumerate(resp['inclusionDistances']):
            distance_int = int(inclusion_dist)
            validator_perf[filter_active_indices[n]] = rate_inclusion_dist(distance_int)
            sum_distance += distance_int
        avg_perf = rate_inclusion_dist(int(round(sum_distance / len(filter_active_indices))))
        return {'perf': validator_perf, 'avg': avg_perf}

    def _get_balance(self, activation_epoch: Dict[str, str]) -> Dict:
        """GET eth/v1alpha1/validator/balances
        Retrieve:
        a) the overall balance for all validators assigned to current_user over time
        b) balance for each individual validators
        """
        cur_epoch = int(self._get_current_epoch())
        balances = {}
        balance_per_index = {i: '0' for i in self.indices}
        total_balance_epoch, balance_per_index = self._balance_for_epoch(
            activation_epoch, cur_epoch
        )
        balances['total'] = total_balance_epoch
        balances['validators'] = balance_per_index
        return balances

    def _balance_for_epoch(
        self, activation_epoch: Dict[str, str], epoch: str
    ) -> Tuple[str, Dict[str, str]]:
        filter_active_indices = [i for i in self.indices if int(activation_epoch[i]) <= int(epoch)]
        if len(filter_active_indices) == 0:
            return '0', {i: '0' for i in self.indices}

        total_balance = 0
        resp = requests.get(
            f'{config.BEACON_RPC_URI}/validators/balances',
            params={'indices': filter_active_indices, 'epoch': epoch},
        )
        resp = resp.json()
        balance_per_index = {}
        for json in resp['balances']:
            total_balance += int(json['balance'])
            balance_per_index[json['index']] = json['balance']
        return total_balance, balance_per_index

    def _get_current_epoch(self) -> str:
        """Calculate the current epoch from genesis"""
        sec_since_genesis = int(time.time()) - config.EPOCH_GENESIS
        current_epoch = int(sec_since_genesis / config.SEC_PER_EPOCH)
        return str(current_epoch)

    # def _get_last_7d_epoch(self) -> List[str]:
    #     pointer_epoch = int(self._get_current_epoch())
    #     last_7d_epoch = [pointer_epoch]
    #     for _ in range(6):
    #         pointer_epoch = max(1, pointer_epoch - config.EPOCH_PER_DAY)
    #         last_7d_epoch = [pointer_epoch] + last_7d_epoch
    #         if pointer_epoch == 0:
    #             break

    #     return last_7d_epoch

    def _get_activation_epoch(self) -> Dict[str, str]:
        """GET /eth/v1alpha1/validators
        Retrieve activation epoch for each validator, None if not activated yet
        """
        resp = requests.get(f'{config.BEACON_RPC_URI}/validators', params={'indices': self.indices})
        resp = resp.json()
        validator_activation_epoch = {}
        for val in resp['validatorList']:
            validator_activation_epoch[val['index']] = val['validator']['activationEpoch']
        return validator_activation_epoch
