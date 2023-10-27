from flask import Flask, jsonify
from mongoengine import Document, StringField, connect
import os

app = Flask(__name__)

# Set the MongoDB URI using the environmental variable
mongodb_uri = os.environ.get('JULIUS_MONGODB_URI')

# Initialize the MongoDB connection
connect(db='mydatabase', host=mongodb_uri)

class User(Document):
    meta = {
        'collection': 'user_details'
    }
    username = StringField(required=True, unique=True)
    email = StringField(required=True, unique=True)

@app.route('/create')
def add_user():
    username = 'Julius Mwash2'
    email = 'cutejuliusmwash@gmail.com2'
    user = User(username=username, email=email)
    user.save()
    return jsonify({"message": f"User {username} added with email {email}"})

@app.route('/', methods=['GET'])
def get_user_data():
    # Retrieve user data from the database
    users = User.objects()

    # Prepare the data as a list of dictionaries
    user_data = [{"username": user.username, "email": user.email} for user in users]

    return jsonify(user_data)

if __name__ == '__main__':
    app.run(debug=True)

