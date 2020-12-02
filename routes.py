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


@app.route('/api/validators/edit', methods=['PUT'])
@jwt_required()
def edit_validators():
    payload = request.json
    indices = payload['indices']
    validator_svc = ValidatorService()
    validator_svc.update(indices, current_identity.id)
    return {'code': HTTPStatus.OK}


@app.route('/protected', methods=["POST"])
@jwt_required()
def protected():
    return '%s' % current_identity.username


@app.route("/api/validators/info", methods=["GET"])
def validators_info():
    pass
