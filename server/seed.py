from app import db, app
from models import User, Illness, Medicine, Order

def create_sample_data():
  with app.app_context():
    

        # Clear existing data
        db.session.query(User).delete()
        db.session.query(Illness).delete()
        db.session.query(Medicine).delete()
        db.session.query(Order).delete()
        db.session.commit()

            
        user1 = User(username='user1', email='user1@example.com', password='password1', name='John Doe', age=25, height=175.0, blood_type='O+',  previous_illnesses=[])
        user2 = User(username='user2', email='user2@example.com', password='password2', name='Jane Dan', age=30, height=160.0, blood_type='A-', previous_illnesses=['Asthma'])
        user3 = User(username='user3', email='user3@example.com', password='password3', name='Peter Smith', age=35, height=180.0, blood_type='B+', previous_illnesses=['Diabetes'])
        user4 = User(username='user4', email='user4@example.com', password='password4', name='Emily Johnson', age=28, height=165.0, blood_type='AB-', previous_illnesses=['None'])
        user5 = User(username='user5', email='user5@example.com', password='password5', name='David Lee', age=40, height=170.0, blood_type='O-', previous_illnesses=['High Blood Pressure'])
        user6 = User(username='user6', email='user6@example.com', password='password6', name='Mary Jackson', age=22, height=158.0, blood_type='A+', previous_illnesses=['None'])
        user7 = User(username='user7', email='user7@example.com', password='password7', name='Robert Williams', age=32, height=185.0, blood_type='B-', previous_illnesses=['Allergies'])
        user8 = User(username='user8', email='user8@example.com', password='password8', name='Sarah Miller', age=27, height=162.0, blood_type='AB+', previous_illnesses=['None'])
        user9 = User(username='user9', email='user9@example.com', password='password9', name='Michael Brown', age=38, height=178.0, blood_type='O+', previous_illnesses=['Arthritis'])
        user10 = User(username='user10', email='user10@example.com', password='password10', name='Jennifer Jones', age=25, height=155.0, blood_type='A-', previous_illnesses=['Migraines'])


        db.session.add_all([user1, user2,user3, user4, user5, user6, user7, user8, user9, user10])
        db.session.commit()

        # Create sample illnesses
        illness1 = Illness(name='Cough', description='Sore throat, coughing, etc.')
        illness2 = Illness(name='Fever', description='High body temperature, chills, etc.')
        illness3 = Illness(name='Headache', description='Pain in the head, throbbing sensations, etc.')
        illness4 = Illness(name='Stomachache', description='Discomfort or pain in the abdominal area, bloating, etc.')
        illness5 = Illness(name='Allergies', description='Sneezing, itching, runny nose, etc.')
        illness6 = Illness(name='Insomnia', description='Difficulty falling or staying asleep, restless nights, etc.')
        illness7 = Illness(name='Back Pain', description='Discomfort or pain in the back, stiffness, etc.')
        illness8 = Illness(name='Common Cold', description='Runny nose, sneezing, coughing, etc.')
        illness9 = Illness(name='Flu', description='Fever, body aches, fatigue, etc.')
        illness10 = Illness(name='Sprained Ankle', description='Injury to the ligaments, swelling, pain, etc.')

        db.session.add_all([illness1, illness2, illness3, illness4, illness5, illness6, illness7, illness8, illness9, illness10])
        db.session.commit()

        # Create sample medicines
        medicine1 = Medicine(name='Cough Syrup', description='Relieves cough symptoms', price=10.0)
        medicine2 = Medicine(name='Fever Reducer', description='Reduces fever and body temperature', price=8.0)
        medicine3 = Medicine(name='Painkillers', description='Relieves headache and body pain', price=15.0)
        medicine4 = Medicine(name='Antacids', description='Alleviates stomachache and acidity', price=12.0)
        medicine5=Medicine(name='Allergy Medication', description='Controls allergy symptoms', price=18.0)
        medicine6 = Medicine(name='Sleep Aid', description='Promotes better sleep and insomnia relief', price=20.0)
        medicine7 = Medicine(name='Back Pain Relief', description='Eases back pain and discomfort', price=25.0)
        medicine8 = Medicine(name='Cold Medicine', description='Treats symptoms of the common cold', price=10.0)
        medicine9 = Medicine(name='Flu Medication', description='Alleviates flu symptoms', price=22.0)
        medicine10 = Medicine(name='Pain Relief Gel', description='Relieves pain from sprained muscles or joints', price=15.0)

        db.session.add_all([medicine1, medicine2, medicine3, medicine4, medicine5, medicine6, medicine7, medicine8, medicine9, medicine10])
        db.session.commit()

       # Assign illnesses to users
        user1.previous_illnesses.extend([illness1, illness3, illness5, illness7, illness9])
        user2.previous_illnesses.extend([illness2, illness4, illness6, illness8, illness10])

        db.session.commit()

        # Assign medicines to illnesses
        illness1.medicines.append(medicine1)
        illness2.medicines.append(medicine2)
        illness3.medicines.append(medicine3)
        illness4.medicines.append(medicine4)
        illness5.medicines.append(medicine5)
        illness6.medicines.append(medicine6)
        illness7.medicines.append(medicine7)
        illness8.medicines.append(medicine8)
        illness9.medicines.append(medicine9)
        illness10.medicines.append(medicine10)

        db.session.commit()

        # Create more sample orders
        order3 = Order(user_id=user1.id, quantity=1, total_price=15.0, delivery_address='789 Elm St', medicine_id=medicine3.id)
        order4 = Order(user_id=user2.id, quantity=3, total_price=36.0, delivery_address='101 Pine St', medicine_id=medicine4.id)
        order5 = Order(user_id=user1.id, quantity=2, total_price=36.0, delivery_address='555 Cedar St', medicine_id=medicine5.id)
        order6 = Order(user_id=user2.id, quantity=1, total_price=20.0, delivery_address='222 Birch St', medicine_id=medicine6.id)
        order7 = Order(user_id=user1.id, quantity=2, total_price=50.0, delivery_address='777 Maple St', medicine_id=medicine7.id)
        order8 = Order(user_id=user2.id, quantity=1, total_price=15.0, delivery_address='333 Oak St', medicine_id=medicine8.id)
        order9 = Order(user_id=user1.id, quantity=3, total_price=66.0, delivery_address='444 Pine St', medicine_id=medicine9.id)
        order10 = Order(user_id=user2.id, quantity=2, total_price=30.0, delivery_address='888 Elm St', medicine_id=medicine10.id)

        db.session.add_all([order3, order4, order5, order6, order7, order8, order9, order10])
        db.session.commit()

if __name__ == '__main__':
    create_sample_data()
