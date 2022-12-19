import os

from flask import Flask, Response, request
from flask_cors import CORS
from flask.templating import render_template
import json
import requests
import random

app = Flask(__name__)
CORS(app)

ITEMS_MICROSERVICE_BASE = os.environ.get("MICROSERVICE1_ADDRESS")
USER_INFO_MICROSERVICE_BASE = os.environ.get("MICROSERVICE2_ADDRESS")
ORDERS_ITEMS_MICROSERVICE_BASE = os.environ.get("MICROSERVICE3_ADDRESS")


@app.route("/")
def landing():
    return json.dumps({"msg": "Welcome to the composite microservice!:",
                       "m1": ITEMS_MICROSERVICE_BASE,
                       "m2": USER_INFO_MICROSERVICE_BASE,
                       "m3": ORDERS_ITEMS_MICROSERVICE_BASE})

@app.route("/create_product", methods=["POST"])
def create_product():
    content = json.loads(request.data)
    print(json.dumps(content))
    product_id = content['product_id']
    name = content['name']
    category = content['category']
    price = content["price"]

    data = {
        "product_id": product_id,
        "name": name,
        "category": category,
        "price": price
    }
    print(f"Creating product with id {product_id}")
    print(f"Going to {USER_INFO_MICROSERVICE_BASE}/create_product")
    print(f"Going to {USER_INFO_MICROSERVICE_BASE}/create_product")
    res = requests.post(f"{ITEMS_MICROSERVICE_BASE}/create_product", data=json.dumps(data))
    res = requests.post(f"{ORDERS_ITEMS_MICROSERVICE_BASE}/create_product", data=json.dumps(data))
    return Response("Addition attempted", status=200, content_type="text/plain")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)