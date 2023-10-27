from flask import Flask, request, jsonify
from datetime import datetime
from mongoengine import connect, Document, StringField, DictField
import os
import json
import random
import uuid

app = Flask(__name__)

# Set the MongoDB connection URI from the environment variable
app.config['MONGODB_SETTINGS'] = {
    'db': 'ordersdatabase',
    'host': os.environ.get('ORDER_JSON_DATABASE_URI')  # Your MongoDB server URI
}

connect(db=app.config['MONGODB_SETTINGS']['db'])

"""
# Set the MongoDB URI using the environmental variable
mongodb_uri = os.environ.get('JULIUS_MONGODB_URI')

# Initialize the MongoDB connection
#connect(db='mydatabase', host=mongodb_uri)
"""





# Define the model
class Order(Document):
    date_time = StringField(required=True)
    json_obj = DictField(required=True)

@app.route('/', methods=['GET'])
def save_order():
    try:
        # Simulate your JSON data
        json_obj = simulate_order_object()

        # Generate the current datetime as a string
        current_datetime = datetime.now()
        date_time = current_datetime.strftime('%Y-%m-%d %H:%M:%S')

        # Create a new Order instance
        order = Order(date_time=date_time, json_obj=json_obj)
        order.save()  # Save the order to MongoDB

        return jsonify({"message": "Order saved successfully!"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400


@app.route('/get_GB_orders', methods=["GET"])
def get_objects():
    pipeline = [
        {
            "$match": {
                "json_obj.shop_name": "Generation Butchery"
            }
        }
    ]

    results = list(Order.aggregate(pipeline))

    obj_data = {}
    count = 1

    for result in results:
        name = f"order_{count}"
        count += 1
        obj_data[name] = result['json_obj']

    return jsonify(obj_data)



"""
@app.route('/get_GB_orders', methods=["GET"])
def get_objects():
    # Define the query to filter by shop_name
    results = Order.objects(json_obj__shop_name='Generation Butchery')
    print(str(results))



    obj_data = {}
    count = 1

    for result in results:
        name = f"order_{count}"
        count += 1
        obj_data[name] = result.json_obj

    return jsonify(obj_data)
"""

def simulate_order_object():
    # Generate a random number for date and UUID for the order key
    num = str(random.randint(0, 59))
    key = str(uuid.uuid4())

    # Define the order details
    order1 = {
        'shop_name': 'Generation Butchery',
        'price_kg': 500,
        'quantity': 4,
        'total_price': 2000,
        'date_time': f"2022-6-{num}15:{num}:12"
    }

    order2 = {
        'shop_name': 'Generation Butchery',
        'price_kg': 600,
        'quantity': 2,
        'total_price': 1200,
        'date_time': f"2023-10-{num}20:{num}:32"
    }

    # Create the order object
    order_obj = {
        key: {
            "order_1": order1,
            "order_2": order2,
            "email": f'example{num}@gmail.com',
            "order_id": f'order{num}'
        }
    }

    json_str = json.dumps(order_obj)
    json_obj = json.loads(json_str)
    return json_obj


if __name__ == "__main__":
    app.run(debug=True, port=5001)

