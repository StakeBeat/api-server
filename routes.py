from http import HTTPStatus

from flask import request

from flaskapp import app
from app.services.user import UserService
from app.services.validator import ValidatorService
from app.services.jwt import jwt_required, current_identity


@app.route("/api/register", methods=["POST"])
def register():
    payload = request.json
    user_svc = UserService()

    user_svc.create(payload)
    return {'code': HTTPStatus.CREATED}


@app.route('/api/validators', methods=['POST'])
@jwt_required()
def add_validators():
    payload = request.json
    indices = payload['indices']
    validator_svc = ValidatorService(current_identity.id)
    validators = validator_svc.create(indices)
    return {'code': HTTPStatus.CREATED, 'validators': validators}


@app.route('/api/validators', methods=['DELETE'])
@jwt_required()
def delete_validators():
    payload = request.json
    indice = payload['index']
    validator_svc = ValidatorService(current_identity.id)
    validator_svc.remove(indice)
    return {'code': HTTPStatus.OK}


@app.route('/api/validators', methods=['GET'])
@jwt_required()
def get_validators():
    validator_svc = ValidatorService(current_identity.id)
    validators = validator_svc.get()
    return {'code': HTTPStatus.OK, 'validators': validators}


@app.route('/protected', methods=["POST"])
@jwt_required()
def protected():
    return '%s' % current_identity.username


@app.route("/api/validators/info", methods=["GET"])
@jwt_required()
def validators_info():
    validator_svc = ValidatorService(current_identity.id)
    info = validator_svc.info()
    return {'code': HTTPStatus.OK, 'validators': info}
