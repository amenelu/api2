from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Resource, Api, reqparse, fields, marshal_with, abort

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
db = SQLAlchemy(app)
api = Api(app)


# User Model
class UserModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(30), unique=True, nullable=False)

    def __repr__(self):
        return f"user(id={self.id}, name={self.name}, email={self.email})"

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
        }


# Request Parser for User
user_args = reqparse.RequestParser()
user_args.add_argument("name", type=str, required=True, help="Name cannot be empty")
user_args.add_argument("email", type=str, required=True, help="Email cannot be blank")

# Field Mapping for Serialization
userFields = {
    "id": fields.Integer,
    "name": fields.String,
    "email": fields.String,
}


# Resource Class for Users
class Users(Resource):
    @marshal_with(userFields)
    def get(self):
        users = UserModel.query.all()
        if not users:
            abort(404, description="No users found.")
        return users

    @marshal_with(userFields)
    def post(self):
        args = user_args.parse_args()  # Fixed missing parentheses
        user = UserModel(name=args["name"], email=args["email"])
        db.session.add(user)
        db.session.commit()
        return user, 201  # Returns the created user with HTTP 201 status


class User(Resource):
    @marshal_with(userFields)
    def get(self, user_id):
        user = UserModel.query.filter_by(id=user_id).first()
        if not user:
            abort(404, description="User not found.")
        return user

    @marshal_with(userFields)
    def put(self, user_id):
        args = user_args.parse_args()
        user = UserModel.query.filter_by(id=user_id).first()
        if not user:
            abort(404, description="User not found.")
        user.name = args["name"]
        user.email = args["email"]
        db.session.commit()
        return user

    def delete(self, user_id):
        user = UserModel.query.filter_by(id=user_id).first()
        if not user:
            abort(404, description="User not found.")

        db.session.delete(user)
        db.session.commit()  # Commit the deletion
        return "", 204


# Adding the Users Resource to API
api.add_resource(Users, "/app/users/")
api.add_resource(User, "/app/users/<int:user_id>")


# Root Route
@app.route("/")
def home():
    return "Welcome to the User API!"


# Run the Application
if __name__ == "__main__":
    db.create_all()  # Ensure tables are created
    app.run(debug=True)
