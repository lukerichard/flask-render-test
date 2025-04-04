#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
from flask import Flask, render_template, request, jsonify, send_from_directory
from flask_pymongo import PyMongo
from werkzeug.security import generate_password_hash, check_password_hash
from bson import ObjectId
from datetime import datetime, timedelta
from models import User, Property, Lease
from config import config

# Initialize Flask app
app = Flask(__name__, static_url_path='', static_folder='static')
app.debug = True

# Load configuration
env = os.getenv('FLASK_ENV', 'development')
app.config.from_object(config[env])

# Set MongoDB URI
app.config["MONGO_URI"] = os.getenv('MONGODB_URI')

# Initialize MongoDB
mongo = PyMongo(app)

@app.route('/test-db')
def test_db():
    try:
        # Try to insert a test document
        test_doc = {'test': True, 'timestamp': datetime.utcnow()}
        result = mongo.db.test_collection.insert_one(test_doc)
        
        # Try to retrieve the document
        retrieved_doc = mongo.db.test_collection.find_one({'_id': result.inserted_id})
        
        # Clean up by removing the test document
        mongo.db.test_collection.delete_one({'_id': result.inserted_id})
        
        return jsonify({
            'status': 'success',
            'message': 'MongoDB connection is working!',
            'details': {
                'inserted_id': str(result.inserted_id),
                'document_retrieved': bool(retrieved_doc)
            }
        })
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': 'MongoDB connection failed',
            'error': str(e)
        }), 500

@app.route('/')
def home():
    return render_template('landing.html')

@app.route('/static/<path:path>')
def send_static(path):
    return send_from_directory('static', path)

# User routes
@app.route('/api/users', methods=['POST'])
def create_user():
    try:
        data = request.get_json()
        
        # Check if user already exists
        if mongo.db.users.find_one({'email': data['email']}):
            return jsonify({'error': 'Email already registered'}), 400
        
        # Create new user
        user = User(
            username=data['username'],
            email=data['email'],
            password_hash=generate_password_hash(data['password']),
            role=data['role'],
            first_name=data.get('first_name'),
            last_name=data.get('last_name'),
            phone=data.get('phone')
        )
        
        result = mongo.db.users.insert_one(user.to_dict())
        return jsonify({'message': 'User created successfully', 'id': str(result.inserted_id)}), 201
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Property routes
@app.route('/api/properties', methods=['GET', 'POST'])
def handle_properties():
    if request.method == 'POST':
        try:
            data = request.get_json()
            property = Property(
                name=data['name'],
                address=data['address'],
                landlord_id=data['landlord_id'],
                description=data.get('description'),
                rent=data.get('rent'),
                status=data.get('status', 'available')
            )
            
            result = mongo.db.properties.insert_one(property.to_dict())
            return jsonify({'message': 'Property created successfully', 'id': str(result.inserted_id)}), 201
        
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    
    else:  # GET request
        try:
            properties = list(mongo.db.properties.find())
            return jsonify([{**prop, '_id': str(prop['_id'])} for prop in properties]), 200
        
        except Exception as e:
            return jsonify({'error': str(e)}), 500

# Lease routes
@app.route('/api/leases', methods=['POST'])
def create_lease():
    try:
        data = request.get_json()
        
        # Validate property and tenant exist
        property = mongo.db.properties.find_one({'_id': ObjectId(data['property_id'])})
        tenant = mongo.db.users.find_one({'_id': ObjectId(data['tenant_id']), 'role': 'tenant'})
        
        if not property or not tenant:
            return jsonify({'error': 'Invalid property or tenant ID'}), 400
        
        lease = Lease(
            property_id=data['property_id'],
            tenant_id=data['tenant_id'],
            start_date=datetime.strptime(data['start_date'], '%Y-%m-%d'),
            end_date=datetime.strptime(data['end_date'], '%Y-%m-%d'),
            rent_amount=data['rent_amount']
        )
        
        # Update property status and tenant
        mongo.db.properties.update_one(
            {'_id': ObjectId(data['property_id'])},
            {'$set': {'status': 'rented', 'tenant_id': ObjectId(data['tenant_id'])}}
        )
        
        result = mongo.db.leases.insert_one(lease.to_dict())
        return jsonify({'message': 'Lease created successfully', 'id': str(result.inserted_id)}), 201
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000) 