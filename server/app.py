from flask import Flask, request, make_response, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from models import db , User, Illness, Medicine, Order, user_illness, illness_medicine


app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False
migrate = Migrate(app, db)

db.init_app(app)


# CRUD actions for User resource
@app.route('/users', methods=['POST'])
def create_user():
    data = request.json
    new_user = User(
        username=data['username'],
        email=data['email'],
        password=data['password'],
        name=data['name'],
        age=data['age'],
        height=data['height'],
        blood_type=data['blood_type'],
        previous_illnesses=data['previous_illnesses']
    )
    db.session.add(new_user)
    db.session.commit()
    return jsonify({'message': 'User created successfully'}), 201

@app.route('/users/<int:id>', methods=['GET'])
def get_user(id):
    user = User.query.filter_by(id=id).first()
    user_data = {
        'id': user.id,
            'username': user.username,
            'email': user.email,
            'name': user.name,
            'age': user.age,
            'height': user.height,
            'blood_type': user.blood_type,
            'previous_illnesses': user.previous_illnesses
    }
   
    return jsonify(user_data)

@app.route('/medicines', methods=['GET'])
def get_medicine():
    medicines = Medicine.query.all()
    medicine_list = []
    for medicine in medicines:
        med_dict={
            'id': medicine.id,
            'name': medicine.name,
            'description': medicine.description,
            'price': medicine.price
        }
        medicine_list.append(med_dict)
    return jsonify(medicine_list)

#route to filter by illness and get medications
@app.route('/illnesses/<string:name>')
def get_illness_medicine(name):
    illness = Illness.query.filter_by(name=name).first()
    if not illness:
        return jsonify({'message' : 'We have not stocked medications for that illness. Check another time'})
    
    illness_data = {
        'id': illness.id,
            'name': illness.name,
            'description': illness.description,
            'medications' : []
            }  
    for medicine in illness.medicines:
        medicine_data= {
            'id': medicine.id,
            'name': medicine.name,
            'description': medicine.description,
            'price': medicine.price
        }
        illness_data['medications'].append(medicine_data)
    return jsonify(illness_data), 200  # jsonify the list of illness data
    



@app.route('/')
def test():
    return ''

if __name__ == '__main__':
    app.run(port=5555)