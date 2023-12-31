from flask import Flask, request, jsonify, session, render_template, url_for
from pymongo import MongoClient
import os
import uuid
import random
import datetime
import time

app = Flask(__name__)
app.secret_key = 'julius_testing_zambezi_mall_project'

# Set up the MongoDB connection
client = MongoClient(os.environ.get('ORDER_JSON_DATABASE_URI'))
db = client['ordersdatabase']



@app.route('/insert_order', methods=["GET"])
def insert_order():
    time_list = [300, 400, 500, 900, 1000, 1400, 1650, 1970, 2000, 2340, 2540, 3000]
    count = 0

    for i in range(0, 300):
        milliseconds = random.choice(time_list)
        seconds = milliseconds / 1000
        time.sleep(seconds)

        # Get the data to insert from the request
        orders_object = list_of_orders_simulation()
        orders_list = simulate_order_object(orders_object)

        collection = db['orders']

        # Insert the data into the collection
        for obj in orders_list:
            result = collection.insert_one(obj)
            if result.acknowledged:
                count += 1
                print("order inserted successfully")
    if count:
        return jsonify({"message": f"{count} orders inserted successfully!"}), 201
    else:
        return jsonify({"error": "Failed to insert order"}), 500



@app.route('/get_GB_orders', methods=["GET"])
def get_objects():
    pipeline = [
        {
            "$match": {
                "json_obj.shop_name": "Jamii Butchery"
            }
        }
    ]

    collection = db['orders']
    results = list(collection.aggregate(pipeline))

    obj_data = {}
    count = 1

    for result in results:
        name = f"order_{count}"
        count += 1
        obj_data[name] = result['json_obj']

    return jsonify(obj_data)



def simulate_order_object(order_data):
    order_obj = {}
    # Generate a random number for date and UUID for the order key
    num = str(random.randint(0, 59))

    hour = str(random.randint(12, 23))
    seconds = str(random.randint(10, 59))
    mili_sec = str(random.randint(10, 59))
    gen_time = f"{hour}:{seconds}:{mili_sec}"

    day = str(random.randint(20, 30))
    gen_date = f"2023-10-{day}"

    gen_date_time = f"{gen_date} {gen_time}"

    timestamp = datetime.datetime.strptime(gen_date_time, "%Y-%m-%d %H:%M:%S").timestamp()

    orders_array = list()

    for key, value in order_data.items():
        value['order_id'] = str(uuid.uuid4())
        # Get the current date
        current_date = datetime.date.today()

        # Convert the current date to a string
        date = current_date.strftime("%Y-%m-%d")
        #date = "2023-10-28"
        email_list = ["juliusmwasstech@gmail.com", "cutejuliusmwash@gmail.com", "mwashlyrics@gmail.com", "gracewambui@gmail.com", "peternjuguna@gmail.com", "oliviawanja@gmail.com", "juliusmwangi@gmail.com"]

        email = random.choice(email_list)


        # Add search/sort array
        ser_sort = [email, gen_date, timestamp] #int(time.time())]

        order_obj = dict()
        value['date_time'] = gen_date_time
        #datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        value['ser_sort'] = ser_sort
        order_obj["order"] = value
        orders_array.append(order_obj)

    return orders_array

def list_of_orders_simulation():
    butch_list = ["Jamii Butchery", "Goshen Butchery", "Generation Butchery", "Meatpoint Butchery", "Gaitho Butchery", "Sammy Butchery", "Wangong Butchery"]
    meat_list = ["Beef", "Mutton", "Pork", "Chicken", "Matumbo", "Fry"]
    price_list = [530.35, 550.87, 600.48, 680.56, 700.76, 800.82, 770.65, 810.15, 900.95]
    total_price_list = [1800, 1500, 890, 650, 3500, 2700, 380, 530, 4100, 2300, 2500, 3250, 3920, 1379, 1820, 1733]

    price_kg = random.choice(price_list)
    total_price = random.choice(total_price_list)
    result = float(total_price) / price_kg
    quantity = round(result, 2)

    orders_list = {
        'order_1': {
            'shop_name': random.choice(butch_list),
            'item_type': random.choice(meat_list),
            'price_kg': str(price_kg),
            'total_price': str(total_price),
            'quantity': str(quantity)
            }
        }
    return orders_list


# Function to set the orders fetch logic (MongoDB)
def fetch_orders_logic():
    # MongoDB orders collection
    collection = db['orders']
    email = "example11@gmail.com"  # Replace with current_user.email

    # Set the number of times the database has to be queried
    if "db_fetch_times" not in session or not session["db_fetch_times"]:
        fetch_times = 0
        remainder = 0
        limit_value = 5

        # Get the total count of documents in the collection
        total_count = collection.count_documents({'order.ser_sort.0': email})
        print(f"total count = {total_count}")

        session["limit_value"] = limit_value
        session['doc_total_count'] = total_count
        session['query_count'] = 0
        session['backward_active'] = False

        # Calculate the number of times to query the database
        if total_count <= limit_value:
            fetch_times = 1
        else:
            fetch_times = int(total_count / limit_value)
            remainder = int(total_count % limit_value)

        if remainder:
            session["db_fetch_times"] = fetch_times + 1
        else:
            session["db_fetch_times"] = fetch_times

    # Set the session to handle database pagination
    if "db_skip_limit" not in session:
        session['db_skip_limit'] = 0

    return 0


@app.route("/fetch_orders", endpoint="fetch_orders_endpoint", methods=["GET"])
def fetch_orders():
    # MongoDB orders collection
    collection = db['orders']

    # Call fetch_orders_logic function
    fetch_orders_logic()

    date = request.args.get("date")
    shop_name = request.args.get("shop_name")
    print(f"shop name = {shop_name}")
    skip = int(request.args.get("skip"))
    sort_order = int(request.args.get("sort_order"))
    email = request.args.get("email")
    no_email = request.args.get("no_email")
    pure_shop = request.args.get("pure_shop")
    email_true = False

    if not email:
        email = "cutejuliusmwass@gmail.com"
    else:
        email_true = True

    print(f"skip: {skip}")
    if not skip:
        print("no skip")
        skip = 0

    # Set an object to hold all the data to be sent to the front-end
    data_obj = dict()

    # Set the limit to the minimum of 5 or the total count
    limit = 20

    if pure_shop:
        print("pure shop")
        results = list(collection.find(
            {'order.shop_name': pure_shop},
            {'_id': 0}).limit(
                limit).skip(skip).sort([('order.ser_sort.2', sort_order)]))
    elif email_true:
        print("email search")
        results = list(collection.find(
            {'order.ser_sort.0': email},
            {'_id': 0}).limit(
                limit).skip(skip).sort([('order.ser_sort.2', sort_order)]))
    elif shop_name and date and no_email:
        print("shop name and date no email")
        results = list(collection.find(
            {'order.shop_name': shop_name, 'order.ser_sort.1': date},
            {'_id': 0}).limit(
                limit).skip(skip).sort([('order.ser_sort.2', sort_order)]))
    elif shop_name and date:
        print("shop name and date")
        results = list(collection.find(
            {'order.ser_sort.0': email, 'order.ser_sort.1': date,
             'order.shop_name': shop_name},
            {'_id': 0}).limit(
                limit).skip(skip).sort([('order.ser_sort.2', sort_order)]))
    elif shop_name:
        print("Only shop name")
        results = list(collection.find(
            {'order.ser_sort.0': email, 'order.shop_name': shop_name},
            {'_id': 0}).limit(
                limit).skip(skip).sort([('order.ser_sort.2', sort_order)]))
        print(str(results))
    elif date and no_email:
        print("date no email")
        results = list(collection.find(
            {'order.ser_sort.1': date},
            {'_id': 0}).limit(
                limit).skip(skip).sort([('order.ser_sort.2', sort_order)]))
    elif date:
        print("Only date")
        results = list(collection.find(
            {'order.ser_sort.0': email, 'order.ser_sort.1': date},
            {'_id': 0}).limit(
                limit).skip(skip).sort([('order.ser_sort.2', sort_order)]))
    else:
        print('default')
        results = list(collection.find(
            #{'order.ser_sort.0': email},
            {'order.ser_sort.0': 'juliusmwasstech@gmail.com'},
            {'_id': 0}).limit(
                limit).skip(skip).sort([('order.ser_sort.2', sort_order)]))

    return jsonify(results)

@app.route('/')
def root():
    return render_template('index.html')








if __name__ == "__main__":
    app.run(debug=True, port=5001)

