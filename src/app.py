import os

from flask import Flask, Response, request
from flask_cors import CORS
from flask.templating import render_template
import json
import requests
import random

app = Flask(__name__)
CORS(app)

ITEMS_MICROSERVICE_BASE = "http://127.0.0.1:5012"
USER_INFO_MICROSERVICE_BASE = "http://127.0.0.1:5011"
#ORDERS_ITEMS_MICROSERVICE_BASE = os.environ("MICROSERVICE3_ADDRESS") #TODO



@app.route("/create_product", methods=["GET", "POST"])
def create_product():
    #login user and see if they have the same user id
    right_data = {"user_id": "gm2962"}
    check_rights = requests.get(f"{USER_INFO_MICROSERVICE_BASE}/is_admin", json=right_data).json()
    if check_rights["is_admin"] == 0:
        return "No admin privilages to add product...Sorry"


    if request.method == 'POST':
        product_id = request.form.get('product_id')
        name = request.form.get('name')
        category = request.form.get('category')
        price = request.form.get("price")

        data = {
            "product_id": product_id,
            "name": name,
            "category": category,
            "price": price
        }
        return requests.post(f"{ITEMS_MICROSERVICE_BASE}/create_product", json=data).json()

    return render_template('add_product.html')

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)