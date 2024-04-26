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

        if budget == None:
            user = session.get(User, getUser())
            budget = Budget(user.id, user.default_budget, user.term)

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

        amount = transaction.amount * (-1)  if transaction.entry else transaction.amount

        budget.budget += amount

        session.delete(transaction)
        session.add(budget)
        session.commit()

        return jsonify(message = "Transacción eliminada de manera correcta"), 200
    
    return jsonify(error = "DT001", message = "La transacción que desea eliminar no existe, tal vez fue eliminada con anterioridad"), 400

@users.route("/getGraphicData", methods=["GET"])
@jwt_required
def getGraphicData():
    try:
        monthWith31Days = [1, 3, 5, 7, 8, 10, 12]
        monthWith30Days =[4, 6, 9, 11]

        labels = []
        payments = [0, 0, 0, 0, 0]
        entrys = [0, 0, 0, 0, 0]
        maxI = 0
        maxG = 0

        budget = getBudgetNow()

        transactions = budget.transactions


        for transaction in transactions:
            date = transaction.date.strftime("%d/%m")
            if date not in labels:
                labels.append(date)

        labelsLen = len(labels)
        if labelsLen < 5:
            
            
            for trans in range(labelsLen, 5):
                dates = labels[0].split("/")
                dates[1] = int(dates[1])
                dates[0] = int(dates[0])
                if dates[0] == 1:
                    dates[1] = dates[1]-1

                    if dates[0] == 0:

                        dates[1] = 12

                        if dates[1] in monthWith31Days:
                            dates[0] = 31
                        elif dates[1] in monthWith30Days:
                            dates[0] = 30
                        else:
                            dates[0] = 28
                    
                else:
                    dates[0] = int(dates[0])-1

                dates[0] = f"0{dates[0]}" if dates[0] < 10 else str(dates[0])
                dates[1] = f"0{dates[1]}" if dates[1] < 10 else str(dates[1])
                date = f"{dates[0]}/{dates[1]}"
                transactionObj = session.query(Transaction).filter(Transaction.date.like(f"%{date}%")).first()

                if transactionObj != None:
                    date = transactionObj.date.strftime("%d/%m")
                    
                labels.insert(0, date)

        labelsLen = len(labels)
        
        if labelsLen > 5:
            dates = [datetime.strptime(date, '%d/%m') for date in labels]
            
            dateMin = min(dates)
            dateMax = max(dates)
            
            salt = (dateMax - dateMin) // 5
            
            ranges = [dateMax - i * salt for i in range(4)]
            
            labels = []
            for date in ranges:
                labels.insert(0, date.strftime('%d/%m'))
            
            labels.insert(0, dateMin.strftime('%d/%m'))

        
        for date in range(len(labels)):
            if date < len(labels)-1:
                entryRange = session.query(Transaction).filter(and_(Transaction.date >= datetime.strptime(labels[date], '%d/%m'), Transaction.date < datetime.strptime(labels[date+1], '%d/%m'), Transaction.entry == True)).all()
                paymentRange = session.query(Transaction).filter(and_(Transaction.date >= datetime.strptime(labels[date], '%d/%m'), Transaction.date < datetime.strptime(labels[date+1], '%d/%m'), Transaction.entry == False)).all()
            else:
                entryRange = session.query(Transaction).filter(and_(Transaction.date >= datetime.strptime(labels[date], '%d/%m'), Transaction.entry == True)).all()
                paymentRange = session.query(Transaction).filter(and_(Transaction.date >= datetime.strptime(labels[date], '%d/%m'), Transaction.entry == False)).all()

            
            entryList = [tr.amount for tr in entryRange]
            entrys[date] = sum(entryList)

            paymentList = [tr.amount for tr in paymentRange]
            payments[date] = sum(paymentList)

        return jsonify(labels = labels, gastos = payments, ingresos = entrys, max_i = max(entrys), max_g = max(payments))
    except Exception as e:
        return jsonify(error = f"{e}")
