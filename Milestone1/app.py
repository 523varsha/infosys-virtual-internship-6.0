from flask import Flask
from flask_cors import CORS
from models import db
from routes import auth_routes
from flask_jwt_extended import JWTManager

app = Flask(__name__)
CORS(app)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["JWT_SECRET_KEY"] = "secretkey"

db.init_app(app)
jwt = JWTManager(app)

app.register_blueprint(auth_routes)

@app.route("/")
def home():
    return {
        "message": "Water Quality Monitor API",
        "status": "Server Running"
    }

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)