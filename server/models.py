from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    name = db.Column(db.String(120))
    age = db.Column(db.Integer)
    height = db.Column(db.Float)
    blood_type = db.Column(db.String(3))
    previous_illnesses = db.relationship('Illness', secondary='user_illness')

    previous_illnesses = db.Column(db.String(300))  

    def add_previous_illness(self, illness_name):
        
        if self.previous_illnesses:
            self.previous_illnesses += f',{illness_name}'
        else:
            self.previous_illnesses = illness_name


class Illness(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    description = db.Column(db.Text)
    medicines = db.relationship('Medicine', secondary='illness_medicine')

class Medicine(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    description = db.Column(db.Text)
    price = db.Column(db.Float)

class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    medicine_id = db.Column(db.Integer, db.ForeignKey('medicine.id'), nullable=False)
    quantity = db.Column(db.Integer)
    total_price = db.Column(db.Float)
    delivery_address = db.Column(db.String(200))

user_illness = db.Table('user_illness',
    db.Column('user_id', db.Integer(), db.ForeignKey('user.id')),
    db.Column('illness_id', db.Integer(), db.ForeignKey('illness.id'))
)

illness_medicine = db.Table('illness_medicine',
    db.Column('illness_id', db.Integer(), db.ForeignKey('illness.id')),
    db.Column('medicine_id', db.Integer(), db.ForeignKey('medicine.id'))
)
