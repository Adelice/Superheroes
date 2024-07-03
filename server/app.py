#!/usr/bin/env python3

from flask import Flask, request, make_response,jsonify,abort
from flask_migrate import Migrate
from flask_restful import Api, Resource
from models import db, Hero, Power, HeroPower
import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DATABASE = os.environ.get(
    "DB_URI", f"sqlite:///{os.path.join(BASE_DIR, 'app.db')}")

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# Set compact mode to False for easier debugging (optional)
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)

@app.route('/')
def index():
    return '<h1>Code challenge</h1>'

@app.route('/heroes', methods=['GET'])
def get_heroes():
    heroes = Hero.query.all()
    serialized_heroes = [hero.to_dict() for hero in heroes]
    return jsonify(serialized_heroes), 200

# Example route to get a specific hero by ID
@app.route('/heroes/<int:id>', methods=['GET'])
def get_hero(id):
    hero = Hero.query.get(id)
    if not hero:
        return jsonify({'error': 'Hero not found'}), 404
    return jsonify(hero.to_dict()), 200

@app.route('/powers', methods=['GET'])
def get_powers():
    # Query all Power objects from the database
    powers = Power.query.all()
    
    # Serialize the powers into a list of dictionaries
    powers_list = [power.to_dict() for power in powers]
    
    # Return the serialized powers as JSON response
    return jsonify(powers_list)
@app.route('/powers/<int:id>', methods=['GET'])
def get_power(id):
    # Query the Power object by its ID
    power = Power.query.get(id)
    
    # If power is None (i.e., not found), return a 404 error
    if power is None:
        abort(404)
    
    # Serialize the power into a dictionary
    power_dict = power.to_dict()
    
    # Return the serialized power as JSON response
    return jsonify(power_dict)

@app.route('/powers/<int:id>', methods=['PATCH'])
def update_power(id):
    power = Power.query.get(id)
    if not power:
        return jsonify({'error': 'Power not found'}), 404

    try:
        data = request.get_json()
        new_description = data.get('description')

        # Validate new description (if necessary)
        if not new_description or len(new_description) < 20:
            return jsonify({'error': 'Description must be at least 20 characters long'}), 400

        # Update power description
        power.description = new_description
        db.session.commit()

        return jsonify({'message': 'Power description updated successfully'}), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500
    finally:
        db.session.close()



if __name__ == '__main__':
    app.run(port=5555, debug=True)
