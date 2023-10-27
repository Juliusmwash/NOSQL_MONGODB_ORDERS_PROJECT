from flask import Flask, jsonify, request, session
from mongoengine import Document, StringField, connect, disconnect, DoesNotExist, EmbeddedDocument, ListField, EmbeddedDocumentField
import os

app = Flask(__name__)

# Set the MongoDB URI using the environmental variable
mongodb_uri = os.environ.get('JULIUS_MONGODB_URI')

# Initialize the MongoDB connection
#connect(db='mydatabase', host=mongodb_uri)

class Specialization(EmbeddedDocument):
    name = StringField(required=True)
    description = StringField()


class User2(Document):
    meta = {
        'collection': 'user_details2'
    }
    username = StringField(required=True, unique=True)
    email = StringField(required=True, unique=True)
    specializations = ListField(EmbeddedDocumentField(Specialization))

@app.route('/create')
def add_user():
    # Connect to the database session
    connect(db='mydatabase', host=mongodb_uri)

    username = 'Julius Mwash2'
    email = 'cutejuliusmwash@gmail.com2'
    user = User2(username=username, email=email)
    user.save()
    # Disconnect from the database session when the request is completed
    disconnect()
    return jsonify({"message": f"User {username} added with email {email}"})


@app.route('/', methods=['GET'])
def get_user_data():
    email = request.args.get('email')  # Get email from the query parameters
    print(f"email = {email}")
    # Connect to the database session
    connect(db='mydatabase', host=mongodb_uri)

    try:
        # Try to retrieve the user based on the provided email
        user = User2.objects.get(email=email)
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


@app.route('/add_data', methods=['GET'])
def add_data():
    key = 'career'
    value = 'software engineering'

    # Connect to the database session
    connect(db='mydatabase', host=mongodb_uri)

    try:
        user = User2.objects.get(email='cutejuliusmwash@gmail.com2')  # Update based on the user's email
        # Create and initialize Specialization instances
        specializations = [
            Specialization(name='Software Engineering', description='Building software applications'),
            Specialization(name='Data Science', description='Analyzing data and creating insights'),
        ]
        user.specializations = specializations
        user.save()
        return jsonify({"message": f"Added {key}: {value} to the user's data"})
    except DoesNotExist:
        return jsonify({"message": "User not found for the given email"})
    finally:
        # Disconnect from the database session when the request is completed
        disconnect()


if __name__ == '__main__':
    app.run(debug=True)

