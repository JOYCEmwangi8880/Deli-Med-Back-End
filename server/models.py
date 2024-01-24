from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
db = SQLAlchemy()

class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    name = db.Column(db.String(120))
    age = db.Column(db.Integer)
    height = db.Column(db.Float)
    blood_type = db.Column(db.String(3))
    previous_illnesses = db.Column(db.String(750)) 
    
    def is_active(self):
        return True
class Illness(db.Model):
    __tablename__ = 'illnesses'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    description = db.Column(db.Text)
    medicines = db.relationship('Medicine', secondary='illness_medicine',
                                primaryjoin='Illness.id==illness_medicine.c.illness_id',
                                secondaryjoin='Medicine.id==illness_medicine.c.medicine_id')

class Medicine(db.Model):
    __tablename__ = 'medicines'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    description = db.Column(db.Text)
    price = db.Column(db.Float)

class Order(db.Model):
    __tablename__ = 'orders'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    quantity = db.Column(db.Integer)
    total_price = db.Column(db.Float)
    delivery_address = db.Column(db.String(200))
    medicine_id = db.Column(db.Integer, db.ForeignKey('medicines.id'), nullable=False)

user_illness = db.Table('user_illness',
    db.Column('user_id', db.Integer(), db.ForeignKey('users.id')),
    db.Column('illness_id', db.Integer(), db.ForeignKey('illnesses.id'))
)

illness_medicine = db.Table('illness_medicine',
    db.Column('illness_id', db.Integer(), db.ForeignKey('illnesses.id')),
    db.Column('medicine_id', db.Integer(), db.ForeignKey('medicines.id'))
)
