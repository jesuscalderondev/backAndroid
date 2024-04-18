from flask import Blueprint, send_file
from database.manager import *
from functions import *
from uuid import UUID

users = Blueprint('users', __name__, static_url_path='users/static/', url_prefix='/users')


@users.route('/getTransactions/<string:month>/<string:year>')
@jwt_required
def getTransactions(month, year):

    transactions = session.query(Transaction).filter(Transaction.user_id == getUser(), Transaction.date.like(f'%{year}-{month}%')).all()

    response = {}
    for i in transactions:
        response[transactions.index(i)] = i.as_dict()

    return jsonify(response = response)

@users.route('/createTransaction', methods = ['POST'])
@jwt_required
def createTransaction():
    try:
        data = request.get_json()

        amount = data['amount']
        entry = True if data['type'] == 'entry' else False
        name = data['name']
        description = data['description']

        budget = getBudgetNow()

        newTransaction = Transaction(budget.id, amount, entry, name, description)

        if not entry:
            amount = amount * -1
        
        budget.budget += amount

        session.add_all([budget, newTransaction])
        session.commit()

        return jsonify(message = 'Se a registrado de manera exitosa su transacción'), 200


    except Exception as e:
        session.rollback()
        return jsonify(error = f'{e}'), 403
    

#terminar ediciones