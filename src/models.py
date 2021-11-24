from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timezone
from utils import APIException

db = SQLAlchemy()


class Crud(object):
    @classmethod
    def create(cls, **kwargs):
        """ Create a new instance"""
        return cls(**kwargs)

    @classmethod
    def get_all(cls):
        """ Get all the instances in db. If there is any error, return None"""
        try:
            return cls.query.all()
        except Exception as error:
            print(error)
            return None

    @classmethod
    def get_by_id(cls, id):
        """ Get an instance in db by id, if it does not exists return None"""
        return cls.query.filter_by(id = id).one_or_none()
    

    def delete(self):
        """ Delete an instance from db """
        try:
            db.session.delete(self)
            db.session.commit()
            return True
        except Exception as error:
            db.session.rollback()
            print(error)
            return False

class Product(db.Model, Crud):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), nullable=False)
    creation_date = db.Column(db.DateTime(timezone=True), nullable=False, default=lambda : datetime.now(timezone.utc))
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'), unique=False, nullable=False)
    price = db.Column(db.String(80), nullable=False, default="0")
    value = db.Column(db.String(80), nullable=False, default="0")
    stock = db.Column(db.String, nullable=False, default="0")

    def __init__(self, **kwargs):
        """ 
        Poducts constructor. Recive keywords arguments and assign it
        """
        if kwargs.get('value') is not None:
            self.value = kwargs.get('value')
        if kwargs.get('price') is not None:
            self.price = kwargs.get('price')
        if kwargs.get('stock') is not None:
            self.stock = kwargs.get('stock')
        self.category_id = kwargs.get('category_id')
        self.name = kwargs.get('name')

    @classmethod
    def create(cls, **kwargs):
        """ 
        Checks the arguments and create a new instance and return it. If there is an error, raise an API exception
        """
        if kwargs.get('name') is None:
            raise APIException('Missing product name', 400)
        if kwargs.get('category_id') is None:
            raise APIException('Missing category', 400)

        return cls(**kwargs)

    def update(self, **kwargs):
        """ 
        Update an instance from db 
        """
        if kwargs.get('name') is not None:
            self.name = kwargs.get('name')
        if kwargs.get('category_id') is not None:
            self.category_id = kwargs.get('category_id')
        if kwargs.get('value') is not None:
            self.value = kwargs.get('value')
        if kwargs.get('price') is not None:
            self.price = kwargs.get('price')
        if kwargs.get('stock') is not None:
            self.stock = kwargs.get('stock')
        
        try:
            db.sesion.commit()
            return True
        except Exception as error:
            db.session.rollback()
            return False


    def __repr__(self):
        return '<Product %r>' % self.name

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "creation_date": self.creation_date,
            "category_id": self.category_id,
            "price": self.price,
            "value": self.value,
            "stock": self.stock
        }


class Category(db.Model, Crud):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(240), nullable=False)
    description = db.Column(db.String(240), nullable=False)
    products = db.relationship('Product', backref='product', uselist=True)
    
    def __init__(self, **kwargs):
        """ 
        Categories constructor. Recive keywords arguments and assign it.
        """
        self.name = kwargs.get('name')
        self.description = kwargs.get('description')

    @classmethod
    def create(cls, **kwargs):
        """
        Checks the arguments and create a new instance and return it. If there is an error, raise an API exception.
        """
        if kwargs.get('name') is None:
            raise APIException('Missing category name', 400)
        if kwargs.get('description') is None:
            raise APIException('Missing category description', 400)
        
        return cls(**kwargs)

    def update(self, **kwargs):
        """ 
        Update an instance from db 
        """
        if kwargs.get('name') is not None:
            self.name = kwargs.get('name')
        if kwargs.get('description') is not None:
            self.category_id = kwargs.get('description')
        
        try:
            db.sesion.commit()
            return True
        except Exception as error:
            db.session.rollback()
            return False

    def __repr__(self):
        return '<Category %r>' % self.name

    def serialize(self):
        """ 
        Represents category instance in a dictionary and return it. 
        """
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "products": [product.serialize() for product in self.products]
        }

