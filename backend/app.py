from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
import requests

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///users.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["JWT_SECRET_KEY"] = "secretkey"

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
jwt = JWTManager(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(200))
    role = db.Column(db.String(50))
    location = db.Column(db.String(100))


class WaterStations(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    location = db.Column(db.String(200))
    latitude = db.Column(db.Numeric)
    longitude = db.Column(db.Numeric)
    managed_by = db.Column(db.String(100))


@app.route("/")
def home():
    return jsonify({
        "message": "Water Quality Monitor & Third Party APIs",
        "status": "Server Running"
    })


@app.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "GET":
        return jsonify({
            "message": "Register API working. Please send POST request."
        })

    data = request.get_json()

    if User.query.filter_by(email=data.get("email")).first():
        return jsonify({"message": "Email already exists"}), 400

    hashed_password = bcrypt.generate_password_hash(
        data["password"]).decode("utf-8")

    new_user = User(
        name=data.get("name"),
        email=data.get("email"),
        password=hashed_password,
        role=data.get("role", "citizen"),
        location=data.get("location")
    )

    db.session.add(new_user)
    db.session.commit()

    return jsonify({"message": "User registered successfully"}), 201


@app.route("/login", methods=["POST"])
def login():

    data = request.get_json()

    user = User.query.filter_by(email=data.get("email")).first()

    if user and bcrypt.check_password_hash(user.password, data.get("password")):

        token = create_access_token(identity=str(user.id))

        return jsonify({
            "token": token,
            "user": {
                "id": user.id,
                "name": user.name,
                "email": user.email,
                "role": user.role,
                "location": user.location
            }
        })

    return jsonify({"message": "Invalid credentials"}), 401


@app.route("/profile", methods=["GET"])
@jwt_required()
def profile():

    current_user_id = get_jwt_identity()
    user = User.query.get(int(current_user_id))

    if not user:
        return jsonify({"message": "User not found"}), 404

    return jsonify({
        "id": user.id,
        "name": user.name,
        "email": user.email,
        "role": user.role,
        "location": user.location
    })


@app.route("/external-water-data", methods=["GET"])
def external_water_data():

    url = "https://api.open-meteo.com/v1/forecast?latitude=17.3850&longitude=78.4867&current_weather=true"

    try:
        response = requests.get(url)
        data = response.json()

        return jsonify({
            "source": "External Environmental API",
            "data": data
        })

    except:
        stations = WaterStations.query.all()

        local_data = []

        for s in stations:
            local_data.append({
                "id": s.id,
                "name": s.name,
                "location": s.location
            })

        return jsonify({
            "source": "Local Database",
            "data": local_data
        })


if __name__ == "__main__":
    with app.app_context():
        db.create_all()

    app.run(debug=True)