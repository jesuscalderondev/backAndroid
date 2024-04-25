from flask import Blueprint
from database.manager import *
from functions import *

users = Blueprint('users', __name__, static_url_path='users/static/', url_prefix='/users')


@users.route('/getTransactions/<string:month>/<string:year>')
@jwt_required
def getTransactions(month, year):
    budgets = session.query(Budget).filter(Budget.user_id == getUser(), or_(Budget.start.like(f'%{year}-{month}%'), Budget.end.like(f'%{year}-{month}%'))).order_by(Budget.end.desc()).all()
    
    response = {}

    for budget in budgets:
        transactions = session.query(Transaction).filter(Transaction.budget_id == budget.id, Transaction.date.like(f'%{year}-{month}%')).all()

        for i in transactions:
            response[transactions.index(i)] = i.as_dict()

    return jsonify(response)


@users.route('/getData')
@jwt_required
def getDataUser():
    return jsonify(session.get(User, getUser()).as_dict())

@users.route('/getBudgetNow')
@jwt_required
def getBudget():
    return jsonify(getBudgetNow().as_dict())

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
            amount = -amount
        
        budget.budget += amount

        session.add_all([budget, newTransaction])
        session.commit()

        return jsonify(message = 'Se a registrado de manera exitosa su transacción'), 200


    except Exception as e:
        session.rollback()
        return jsonify(error = f'{e}'), 403
    
@users.route("/deleteTransaction/<string:id>", methods=['GET'])
@jwt_required
def deleteTransaction(id):
    transaction = session.get(Transaction, UUID(id))

    if transaction != None:
        budget = session.get(Budget, transaction.budget_id)

        budget.budget += transaction.amount * (-1)

        session.delete(transaction)
        session.add(budget)
        session.commit()

        return jsonify(message = "Transacción eliminada de manera correcta")
    
    return jsonify(error = "DT001", message = "La transacción que desea eliminar no existe, tal vez fue eliminada con anterioridad")
