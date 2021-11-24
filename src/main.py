"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, Category, Product
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DB_CONNECTION_STRING')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/categories', methods=['GET', 'POST'])
@app.route('/categories/<int:category_id>', methods=['GET', 'PUT', 'DELETE'])
def handle_categories(category_id=None):
    if request.method == 'GET':
        if category_id is None:
            #If GET is request without a id
            categories = Category.get_all()
            response_body = {
                "categories": [category.serialize() for category in categories]
            }
            return jsonify(response_body), 200
        #If get is request with an id, check if exists
        category = Category.get_by_id(category_id)
        if category is not None: 
            return jsonify({
                "category" : category.serialize()
            }), 200
        else:
            return jsonify({"message": "category was not found" }), 404
    if request.method == 'PUT':
        #PUT is always request with a category_id
        request_body = request.json
        if category_id is None:
            return jsonify({"message": "Category id was not send, try again"}), 400
        if request_body.get('name') is None or request_body.get('description') is None:
            return jsonify({
                "message": "Please send name and description even if it stills the same."
            }), 400
        category = Category.get_by_id(category_id)
        is_updated = category.update(
            name = request_body['name'],
            description = request_body['description']
        )
        #The update method return True if everything is ok. Else, return False and raise and error.
        if is_updated:
            return jsonify([]), 204
        else:
            return jsonify({
                "message": "An error occur while updating the resource, try again"
            }), 500
    if request.method == 'POST':
        request_body = request.json
        if request_body.get('name') is None or request_body.get('description') is None:
            return jsonify({
                "message": "Please send name and description. Check documentation for more information"
            }), 400
        new_category = Category.create(
            name = request_body['name'],
            description = request_body['description']
        )
        #If new_category is no an instance of Category is because something happened
        if not isinstance(new_category, Category):
            return josinfy({
                "message": "Something happend while creating the category, try again"
            }), 500
        is_save = new_category.save()
        if is_save:
            return jsonify([]), 201
        else:
            return jsonify({
                "message": "Something happened while saving on database, try again"
            }), 500
    #Else, request method is DELETE
    category= Category.get_by_id(category_id)
    if category is None:
        return jsonify({
            "message": "Category not found"
        }), 404
    is_deleted = category.delete()
    if is_deleted:
        return jsonify([]), 200
    else:
        return jsonify({
            "message": "Something happened trying to delete, please try again"
        }), 500

@app.route('/products', methods=['GET', 'POST'])
@app.route('/products/<int:product_id>', methods=['GET', 'PUT', 'DELETE'])
def handle_products(product_id=None):
    if request.method == 'GET':
        #If product_id is None, request all the products
        if product_id is None:
            products = Product.get_all()
            return jsonify({
                "products": [ product.serialize() for product in products]
            }), 200
        #GET poduct by id
        product = Product.get_by_id(id = product_id)
        if product is None:
            return jsonify({"message": "product was not found" }), 404
        return jsonify({
            "product" : product.serialize()
        }), 200
    if request.method == 'POST':
        request_body = request.json
        product = Product.create(**request_body)
        print(product)
        
        return jsonify(product.serialize()), 200
    
    if request.method == 'PUT':
        pass
    if request.method == 'DELETE':
        pass


# this only runs if `$ python src/main.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3500))
    app.run(host='0.0.0.0', port=PORT, debug=False)
