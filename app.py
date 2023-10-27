from flask import Flask, render_template, jsonify
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

@app.route('/')
def add_user():
    username = 'Julius Mwash'
    email = 'cutejuliusmwash@gmail.com'
    user = User(username=username, email=email)
    user.save()
    return jsonify({"message":f"User {username} added with email {email}"})

if __name__ == '__main__':
    app.run(debug=True)

