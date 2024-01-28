from flask import Flask, request, jsonify, make_response
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from models import db, User, Illness, Medicine, Order, user_illness, illness_medicine
from auth import auth
from flask_cors import CORS

app = Flask(__name__)

app.config['SECRET_KEY'] = 'your_unique_and_secret_key'

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JSONIFY_COMPACT'] = False  
migrate = Migrate(app, db)
CORS(app)
db.init_app(app)

login_manager = LoginManager()
login_manager.init_app(app)
app.register_blueprint(auth, url_prefix='/auth')

# Configure user loader function
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

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



@app.route('/users', methods=['GET'])
def get_users():
    users = User.query.all()
    user_list = []

    for user in users:
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
        user_list.append(user_data)

    return jsonify(user_list)

@app.route('/users/<int:id>', methods=['PATCH'])
def update_user(id):
    user = User.query.get(id)
    if not user:
        return jsonify({'message': 'No user found'}), 404

    data = request.json
    user.username = data.get('username', user.username)
    user.email = data.get('email', user.email)
    user.name = data.get('name', user.name)
    user.age = data.get('age', user.age)
    user.height = data.get('height', user.height)
    

    db.session.commit()
    return jsonify({'message': 'User updated successfully'}), 200

@app.route('/users/<int:id>', methods=['DELETE'])
def delete_user(id):
    user = User.query.get(id)
    if not user:
        return jsonify({'message': 'No user found'}), 404

    db.session.delete(user)
    db.session.commit()
    return jsonify({'message': 'User deleted successfully'}), 200

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

# Retrieve information about a specific medicine by ID
@app.route('/medicines/<int:id>', methods=['GET'])
def get_medicine_by_id(id):
    medicine = Medicine.query.get(id)
    if not medicine:
        return jsonify({'message': 'Medicine not found'}), 404

    medicine_data = {
        'id': medicine.id,
        'name': medicine.name,
        'description': medicine.description,
        'price': medicine.price
    }

    return jsonify(medicine_data), 200

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

@app.route('/orders', methods=['POST'])
def create_order():
    data = request.json
    user = User.query.get(data['user_id'])
    medicine = Medicine.query.get(data['medicine_id'])

    
    new_order = Order(
        user_id=user.id,
        medicine_id=medicine.id,
        quantity=data['quantity'],
        total_price=data['total_price'],
        delivery_address=data['delivery_address']
    )
    db.session.add(new_order)

    
    user.add_previous_illness(medicine.illnesses[0].name)

    db.session.commit()
    return jsonify({'message': 'Order created successfully'}), 201


@app.route('/orders/<int:id>', methods=['GET'])
def get_order(id):
    order = Order.query.filter_by(id=id).first()
    order_data = {
        'id': order.id,
        'user_id': order.user_id,
        'medicine_id': order.medicine_id,
        'quantity': order.quantity,
        'total_price': order.total_price,
        'delivery_address': order.delivery_address
    }
    return jsonify(order_data)


@app.route('/orders/user/<int:user_id>', methods=['GET'])
def get_previous_orders(user_id):
    orders = Order.query.filter_by(user_id=user_id).all()
    previous_orders = []

    for order in orders:
        order_data = {
            'id': order.id,
            'user_id': order.user_id,
            'medicine_id': order.medicine_id,
            'quantity': order.quantity,
            'total_price': order.total_price,
            'delivery_address': order.delivery_address
        }
        previous_orders.append(order_data)

    return jsonify(previous_orders)
    

@app.route('/orders/<int:id>', methods=['PUT'])
def update_order(id):
    order = Order.query.get(id)
    if not order:
        return jsonify({'message': 'No order found'}), 404

    data = request.json
    order.user_id = data.get('user_id', order.user_id)
    order.medicine_id = data.get('medicine_id', order.medicine_id)
    order.quantity = data.get('quantity', order.quantity)
    order.total_price = data.get('total_price', order.total_price)
    order.delivery_address = data.get('delivery_address', order.delivery_address)

    db.session.commit()
    return jsonify({'message': 'Order updated successfully'}), 200

@app.route('/orders/<int:id>', methods=['DELETE'])
def delete_order(id):
    order = Order.query.get(id)
    if not order:
        return jsonify({'message': 'No order found'}), 404

    db.session.delete(order)
    db.session.commit()
    return jsonify({'message': 'Order deleted successfully'}), 200

@app.route('/illnesses', methods=['GET'])
def get_illnesses():
    illnesses = Illness.query.all()
    illness_list = []

    for illness in illnesses:
        illness_data = {
            'id': illness.id,
            'name': illness.name,
            'description': illness.description
        }
        illness_list.append(illness_data)

    return jsonify(illness_list)

    
@app.route('/illnesses/<int:illness_id>/medicines', methods=['GET'])
def get_medicines_for_illness(illness_id):
    illness = Illness.query.get(illness_id)
    print("Illness:", illness)  # Debug print statement
    
    if not illness:
        return jsonify({'error': 'Illness not found'}), 404
    
    medicines = illness.medicines
    print("Medicines:", medicines)  # Debug print statement
    
    serialized_medicines = [medicine.serialize() for medicine in medicines]
    print("Serialized Medicines:", serialized_medicines)  # Debug print statement
    
    return jsonify(serialized_medicines)


@app.route('/')
def test():
    return ''

if __name__ == '__main__':
    app.run(debug=True)