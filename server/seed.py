from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from faker import Faker
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

# ... (rest of the functions remain unchanged)
