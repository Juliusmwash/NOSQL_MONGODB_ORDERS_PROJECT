from flask import Flask, jsonify, request, session
from mongoengine import Document, StringField, connect, disconnect, DoesNotExist
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
    email = request.args.get('email')  # Get email from the query parameters
    print(f"email = {email}")
    # Connect to the database session
    connect(db='mydatabase', host=mongodb_uri)

    try:
        # Try to retrieve the user based on the provided email
        user = User.objects.get(email=email)
        user_data = {
            "username": user.username,
            "email": user.email
        }
        return jsonify(user_data)
    except DoesNotExist:
        return jsonify({"message": "User not found for the given email"})
    finally:
        # Disconnect from the database session when the request is completed
        disconnect()

if __name__ == '__main__':
    app.run(debug=True)

