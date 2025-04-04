from datetime import datetime
from bson import ObjectId

class User:
    def __init__(self, username, email, password_hash, role, first_name=None, last_name=None, phone=None):
        self.username = username
        self.email = email
        self.password_hash = password_hash
        self.role = role  # 'landlord' or 'tenant'
        self.first_name = first_name
        self.last_name = last_name
        self.phone = phone
        self.created_at = datetime.utcnow()
        self.updated_at = datetime.utcnow()

    def to_dict(self):
        return {
            'username': self.username,
            'email': self.email,
            'role': self.role,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'phone': self.phone,
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }

class Property:
    def __init__(self, name, address, landlord_id, description=None, rent=None, status='available'):
        self.name = name
        self.address = address
        self.landlord_id = ObjectId(landlord_id)
        self.description = description
        self.rent = rent
        self.status = status  # 'available', 'rented', 'maintenance'
        self.tenant_id = None
        self.created_at = datetime.utcnow()
        self.updated_at = datetime.utcnow()

    def to_dict(self):
        return {
            'name': self.name,
            'address': self.address,
            'landlord_id': str(self.landlord_id),
            'description': self.description,
            'rent': self.rent,
            'status': self.status,
            'tenant_id': str(self.tenant_id) if self.tenant_id else None,
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }

class Lease:
    def __init__(self, property_id, tenant_id, start_date, end_date, rent_amount, status='active'):
        self.property_id = ObjectId(property_id)
        self.tenant_id = ObjectId(tenant_id)
        self.start_date = start_date
        self.end_date = end_date
        self.rent_amount = rent_amount
        self.status = status  # 'active', 'expired', 'terminated'
        self.created_at = datetime.utcnow()
        self.updated_at = datetime.utcnow()

    def to_dict(self):
        return {
            'property_id': str(self.property_id),
            'tenant_id': str(self.tenant_id),
            'start_date': self.start_date,
            'end_date': self.end_date,
            'rent_amount': self.rent_amount,
            'status': self.status,
            'created_at': self.created_at,
            'updated_at': self.updated_at
        } 