from flask import Flask, request, jsonify
from flask import session as cookies
from dotenv import load_dotenv
from flask_cors import CORS
from datetime import datetime, timedelta
from jwt import encode
import re
import os

from database.manager import *
from functions import *

load_dotenv()

app = Flask(__name__)
app.config["SECRET_KEY"] = os.environ["SECRET_KEY"]

CORS(app, origins=['*'], supports_credentials=True)


@app.route('/login', methods = ['POST'])
def login():
    try:
        try:
            data = request.get_json()
        except:
            data = request.form

        email = data['email']
        password = data['password']

        user = session.query(User).filter(User.email == email).first()

        if user != None and passwordVerify(user.password, password):
            token = creatreJWT(user.id)
            cookies.setdefault("token", token)
            return jsonify(token = token), 200
        else:
            return jsonify(error = 'Incorrect credentials', message = 'El correo o contraseña son incorrectos, verifique e intente nuevamente.'), 401
    except Exception as e:
        print(e)
        return jsonify({'error': f'{e}', 'data' : data}), 403


@app.route('/register', methods = ['POST'])
def register():

    try:
        data = request.get_json()
        print(data)
        newUser = User(data['email'], passwordHash(data['password']), data['first_name'], data['last_name'], data['budget'], data['term'])

        firstBudget = Budget(newUser.id, newUser.default_budget, newUser.term)

        session.add_all([newUser, firstBudget])
        session.commit()

        token = creatreJWT(newUser.id)


        return jsonify(token = token), 200
    except Exception as e:
        session.rollback()
        return jsonify(error = f'{e}'), 400

from users.manager import users

app.register_blueprint(users)

if __name__ == '__main__':
    Base.metadata.create_all(engine)
    app.run(debug=True)