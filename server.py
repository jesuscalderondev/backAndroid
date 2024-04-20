from flask import Flask, request, jsonify, abort
from flask import session as cookies
from dotenv import load_dotenv
from flask_cors import CORS
from sqlalchemy.exc import *
from jwt import encode
import re
import os


from database.manager import *
from functions import *

app = Flask(__name__)

load_dotenv()

app.config["SECRET_KEY"] = os.environ["SECRET_KEY"]

CORS(app, origins='*', supports_credentials=True)

blocked_ips = []

@app.before_request
def block_ip():
    client_ip = request.remote_addr
    if client_ip in blocked_ips:
        abort(403)

@app.route("/")
def testAbort():
    abort(500)

@app.route('/login', methods = ['POST'])
def login():
    try:
        data = request.get_json()

        email = data['email']
        password = data['password']

        user = session.query(User).filter(User.email == email).first()

        if user != None and passwordVerify(user.password, password):
            token = creatreJWT(user.id)
            return jsonify(token = token), 200
        else:
            return jsonify(error = 'L001', message = 'El correo o contraseña son incorrectos, verifique e intente nuevamente.'), 403
    except Exception as e:
        return jsonify(error = 'L000', details = f'{e}', message = 'Se ha producido un error a la hora de enviar los datos, verificar el parametro de details'), 403
    


@app.route('/register', methods = ['POST'])
def register():

    try:

        print(request.remote_addr)
        print(request.__dict__)
        data = request.get_json()
        
        if type(data['term']) == float:
            raise StatementError("Se ha detectado un tipo de dato incorrecto", None, None, None)
        
        if len(data) > 6:
            raise Exception("Has enviado más datos de los requeridos... pedimos por favor no repetir esta acción :)")

        newUser = User(data['email'], passwordHash(data['password']), data['first_name'], data['last_name'], data['budget'], data['term'])

        firstBudget = Budget(newUser.id, newUser.default_budget, newUser.term)

        session.add_all([newUser, firstBudget])
        session.commit()

        token = creatreJWT(newUser.id)

        return jsonify(token = token), 200
        

    except (IntegrityError, StatementError, KeyError, Exception) as e:
        session.rollback()
        if isinstance(e, IntegrityError):
            error = 'R001'
            message = 'Este correo ya fue usado con anterioridad'

        elif isinstance(e, StatementError):
            error = 'R002'
            message = 'No se admiten letras ni números con comas o puntos en el campo de duración del presupuesto'
        
        elif isinstance(e, KeyError):
            error = 'R003'
            message = f'Falta el valor para {e} en su petición'

        elif isinstance(e, Exception):
            error = 'R004'
            message = f'{e}'
            blocked_ips.append(request.remote_addr)

        return jsonify(error = error, message = message), 400

@app.errorhandler(403)
def errorHandler(e):
    return jsonify(error = 'EH403', message = 'Usted ha sido bloqueado de nuestro servicio debido a un comportamiento indebido, si la decisión no le parece justa, comuniquese con nuestro soporte')

@app.errorhandler(404)
def errorHandler(e):
    return jsonify(error = 'EH404', message = 'La ruta a la que intenta acceder no existe, verifique la url')

@app.errorhandler(405)
def errorHandler(e):
    return jsonify(error = 'EH405', message = f'El método {request.method} no es válido para esta url')

@app.errorhandler(415)
def errorHandler(e):
    return jsonify(error = 'EH415', message = f'No se ha enviado el tipo de petición correcta verifique que en el header existe *application/json*')

@app.errorhandler(500)
def errorHandler(e):
    return jsonify(error = 'EH500', message = 'Hubo un fallo interno en el servidor, comunicarse con el soporte si el error existe')

from users.manager import users

app.register_blueprint(users)
Base.metadata.create_all(engine)

if __name__ == '__main__':
    app.run(debug=True)