from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from faker import Faker
from random import choice as rc  # Add this import
from models import db, User, Illness, Medicine, Order, user_illness, illness_medicine

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

fake = Faker()
app.app_context().push()

def create_fake_user():
    return User(
        username=fake.user_name(),
        email=fake.email(),
        password=fake.password(),
        name=fake.name(),
        age=fake.random_int(min=18, max=80),
        height=fake.random.uniform(150, 200),
        blood_type=fake.random_element(elements=('A', 'B', 'AB', 'O')),
        previous_illnesses=fake.text(max_nb_chars=750)
    )

illness_names = ["Fever", "Common Cold", "Headache", "Flu", "Stomachache"]
illness_descriptions = [
    "A common symptom of various illnesses characterized by an elevated body temperature.",
    "A mild viral infection affecting the nose and throat.",
    "A pain in the head or upper neck.",
    "A highly contagious respiratory infection.",
    "Pain or discomfort in the stomach."
]

def create_fake_illness():
    return Illness(
        name=rc(illness_names),
        description=rc(illness_descriptions)
    )

def create_fake_medicine():
    return Medicine(
        name=fake.word(),
        description=fake.text(),
        price=fake.pyfloat(min_value=5, max_value=50, right_digits=2)
    )

def create_fake_order():
    return Order(
        user_id=fake.random_int(min=1, max=10),
        medicine_id=fake.random_int(min=1, max=20),
        quantity=fake.random_int(min=1, max=10),
        total_price=fake.pyfloat(min_value=5, max_value=500, right_digits=2),
        delivery_address=fake.address()
    )

def seed_database():
    fake_users = [create_fake_user() for _ in range(10)]
    fake_illnesses = [create_fake_illness() for _ in range(10)]
    fake_medicines = [create_fake_medicine() for _ in range(20)]
    fake_orders = [create_fake_order() for _ in range(10)]

    db.create_all()

    db.session.bulk_save_objects(fake_users)
    db.session.bulk_save_objects(fake_illnesses)
    db.session.bulk_save_objects(fake_medicines)
    db.session.bulk_save_objects(fake_orders)

    db.session.commit()

if __name__ == '__main__':
    seed_database()
