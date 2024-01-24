
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

@app.route('/')
def test():
    return 'Pizzas Inn'

if __name__ == '__main__':
    app.run(port=5555)

