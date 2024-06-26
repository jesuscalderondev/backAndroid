from werkzeug.security import generate_password_hash, check_password_hash
from flask import request, jsonify
from functools import wraps
from jwt import ExpiredSignatureError, InvalidTokenError, decode, encode
from datetime import datetime, timedelta
import os
from dotenv import load_dotenv
from uuid import UUID
from database.manager import *


load_dotenv()

def passwordHash(password:str):
    return generate_password_hash(password)

def passwordVerify(passHash:str, passUnHashed:str):
    return check_password_hash(passHash, passUnHashed)

def creatreJWT(id):
    payload = {
        'id': str(id),
        'exp': datetime.utcnow() + timedelta(hours=1)
    }

    return encode(payload, os.environ["SECRET_KEY"], algorithm='HS256')

def jwt_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization').split(" ")[1]

        if not token:
            return jsonify({'error': 'Falta el token'}), 401

        try:
            payload = decode(token, os.environ["SECRET_KEY"], algorithms=['HS256'])
        except (ExpiredSignatureError, InvalidTokenError) as e:
            if isinstance(e, ExpiredSignatureError):
                return jsonify(error = 'T001', message = 'El token que ha proporcionado se encuentra vencido'), 401
            elif isinstance(e, InvalidTokenError):
                return jsonify(error = 'T000', message = 'El token que ha enviado no es válido'), 401
        return f(*args, **kwargs)

    return decorated

def getUser():
    token = request.headers.get('Authorization').split(" ")[1]
    payload = decode(token, os.environ["SECRET_KEY"], algorithms=['HS256'])
    return UUID(payload.get('id'))

def getBudgetNow() -> Budget:
    budget = session.query(Budget).filter(and_(Budget.start <= datetime.now().date(), Budget.end > datetime.now().date(), Budget.user_id == getUser())).first()
    return budget