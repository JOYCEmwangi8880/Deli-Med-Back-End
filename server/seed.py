from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from faker import Faker
import random  # Import random module for generating random data
from models import db, User, Illness, Medicine, user_illness, illness_medicine

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

fake = Faker()  # Initialize Faker for generating fake data

def create_fake_user():
    user = User(
        username=fake.user_name(),
        email=fake.email(),
        password=fake.password(),
        name=fake.name(),
        age=fake.random_int(min=18, max=80),
        height=fake.random.uniform(150, 200),
        blood_type=fake.random_element(elements=('A', 'B', 'AB', 'O')),
        previous_illnesses=fake.text(max_nb_chars=750)
    )
    return user

def create_fake_illness():
    return Illness(
        name=fake.word(),
        description=fake.text(max_nb_chars=200)
    )

def create_fake_medicine():
    return Medicine(
        name=fake.word(),
        description=fake.text(max_nb_chars=200),
        price=random.uniform(5.0, 100.0)
    )

def seed_database():
    with app.app_context():
        # Delete all records from tables
        db.session.query(User).delete()
        db.session.query(Illness).delete()
        db.session.query(Medicine).delete()
        db.session.query(user_illness).delete()
        db.session.query(illness_medicine).delete()

        # Commit the deletion
        db.session.commit()

        # Create custom data for illnesses and medicines
        custom_illnesses = [
            Illness(name="fever", description="Rise in body temperatures"),
            Illness(name="headache", description="Pain from the forehead back to your neck"),
            Illness(name="stomachache", description="Pain around abdominal areas"),
            Illness(name="toothache", description="Pain from your teeth or areas around the gums"),
            Illness(name="asthma", description="Difficulty in breathing")
        ]

        custom_medicines = [
            Medicine(name="FeverFix", description="FeverFix is an effective medication for reducing fever caused by various infections and illnesses.", price=10.0),
            Medicine(name="HeadacheRelief", description="HeadacheRelief provides rapid relief from headaches and migraines", price=20.0),
            Medicine(name="StomachSoothe", description="StomachSoothe is a gentle yet effective remedy for soothing stomach aches and digestive discomfort", price=30.0),
            Medicine(name="ToothEase", description="ToothEase provides fast relief from toothache and dental discomfort", price=40.0),
            Medicine(name="AsthmaEase", description="AsthmaEase is a trusted medication for managing asthma symptoms and improving respiratory health", price=50.0)
        ]

        # Add custom data to the database session
        db.session.add_all(custom_illnesses)
        db.session.add_all(custom_medicines)
        db.session.commit()

        # Associate illnesses with appropriate medicines
        for illness in custom_illnesses:
            if illness.name == "fever":
                illness.medicines.append(custom_medicines[0])  # Associate FeverFix with fever
            elif illness.name == "headache":
                illness.medicines.append(custom_medicines[1])  # Associate HeadacheRelief with headache
            elif illness.name == "stomachache":
                illness.medicines.append(custom_medicines[2])  # Associate StomachSoothe with stomachache
            elif illness.name == "toothache":
                illness.medicines.append(custom_medicines[3])  # Associate ToothEase with toothache
            elif illness.name == "asthma":
                illness.medicines.append(custom_medicines[4])  # Associate AsthmaEase with asthma

        # Create fake users and associate them with custom illnesses
        fake_users = [create_fake_user() for _ in range(10)]

        for user in fake_users:
            for _ in range(random.randint(1, 3)):
                illness = random.choice(custom_illnesses)
                user.illnesses.append(illness)

        db.session.add_all(fake_users)
        db.session.commit()

if __name__ == '__main__':
    seed_database()
