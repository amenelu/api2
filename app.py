from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Resource, Api, reqparse, fields, marshal_with, abort

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
db = SQLAlchemy(app)
api = Api(app)


class UserModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(30), unique=True, nullable=False)

    def __repr__(self):
        return f"user(name={self.name},email={self.email})"


user_args = reqparse.RequestParser()
user_args.add_argument("name", type=str, required=True, help="name can not be empty")
user_args.add_argument("email", type=str, required=True, help="email can not be blank")

userFields = {"id": fields.Integer, "name": fields.String, "email": fields.String}


class Users(Resource):
    @marshal_with(userFields)
    def get(self):
        users = UserModel.query.all()
        return users

    def post(self):
        args = user_args.parse_args()
        user = UserModel(name=args["name"], email=args["email"])
        db.session.add(user)
        db.session.commit()
        Users = UserModel.query.all()
        return user, 201


api.add_resource(Users, "/app/users/")


@app.route("/")
def home():
    return ""


if __name__ == "__main":
    app.run(debug=True)
