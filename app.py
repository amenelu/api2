from flask import Flask
from sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
db = SQLAlchemy(app)


class UserModel(db.model):
    id = db.column(db.Integer, primarykey=True)
    name = db.column(db.string(80), unique=True, nullable=False)
    email = db.column(db.string(30), unique=True, nullable=False)

    def __repr__(self):
        return f"user(name={self.name},email={self.email})"


@app.route("/")
def home():
    return ""


if __name__ == "__main":
    app.run(debug=True)
