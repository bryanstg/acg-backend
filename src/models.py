from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timezone

db = SQLAlchemy()

""" 
Tabla Categoría debe contener: id, nombre y descripción.
id -> int 
nombre -> str
descripción -> str
Tabla Producto debe contener: id, fecha creación, nombre, categoría, precio, valor, stock
id-> int ✅
fecha_creacion -> date ✅
nombre -> str ✅
categoria_id -> int ✅
precio -> int ✅
valor -> int ✅
stock -> int ✅
"""

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), nullable=False)
    creation_date = db.Column(db.Datetime(timezone=True), nullable=False, default=lambda : datetime.now(timezone.utc))
    category_id = db.Column(db.Integer, db.ForeignKey('category.id') unique=False, nullable=False)
    price = db.Column(db.String(80), nullable=False, default=0)
    value = db.Column(db.String(80), nullable=False, default=0)
    stock = db.Column(db.Integer, nullable=False, default=0)

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


class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Colum(db.String(240), nullable=False)
    description = db.Column(db.String(240), nullable=False)
    products = db.relationship('Product', backref='product', uselist=True)

    def __repr__(self):
        return '<Category %r>' % self.name

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "products": [product.serialize() for product in self.products]
        }

