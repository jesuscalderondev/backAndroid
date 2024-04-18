from sqlalchemy import Integer, String, Uuid, Double, Column, Boolean, DateTime, ForeignKey, Date
from sqlalchemy.orm import declarative_base, sessionmaker, relationship, backref
from sqlalchemy import create_engine, and_, or_
from datetime import datetime, timedelta
from uuid import uuid4


url = f'sqlite:///database.sqlite'
engine = create_engine(url)
Session = sessionmaker(bind=engine)
session = Session()

Base = declarative_base()


class User(Base):

    __tablename__ = 'Users'

    id = Column(Uuid, primary_key=True, unique=True, nullable=False)
    email = Column(String(225), nullable=False, unique=True)
    password = Column(String(300), nullable=False)
    first_name = Column(String(225), nullable=False)
    last_name = Column(String(225), nullable=False)
    default_budget = Column(Double, nullable=False)
    term = Column(Integer, nullable=False)
    active = Column(Boolean, nullable=False, default=True)

    budgets = relationship("Budget", backref="user")


    def __init__ (self, email, password, first_name, last_name, budget, term):

        self.id = uuid4()
        self.email = email
        self.password = password
        self.first_name = first_name
        self.last_name = last_name
        self.default_budget = budget
        self.term = term

        firstBudget = Budget(self.id, self.default_budget, self.term)

        session.add(firstBudget)

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}
    

class Budget(Base):
    __tablename__ = 'Budgets'
    id = Column(Uuid, primary_key=True, unique=True, nullable=False)
    budget = Column(Double, nullable=False)
    start = Column(Date, nullable=False)
    end = Column(Date, nullable=False)
    user_id = Column(Uuid, ForeignKey('Users.id'))

    transactions = relationship("Transaction", backref="budget")

    def __init__ (self, userId, budget, term):
        self.user_id = userId
        self.budget = budget
        self.start = datetime.now().date()
        self.end = self.start + timedelta(days=term)


class Transaction(Base):
    __tablename__ = 'Transactions'

    id = Column(Uuid, primary_key=True, unique=True, nullable=False)
    amount = Column(Double(2), nullable=False)
    date = Column(DateTime, nullable=False)
    entry = Column(Boolean, nullable=False)
    name = Column(String(225), nullable=False)
    description = Column(String(2000), nullable=True)

    budget_id = Column(Uuid, ForeignKey('Budgets.id'))

    def __init__ (self, budgetId, amount, entry, name, description):

        self.id = uuid4()
        self.budget_id = budgetId
        self.amount = amount
        self.entry = entry
        self.name = name
        self.description = description
        self.date = datetime.now()

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}