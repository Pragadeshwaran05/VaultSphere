from flask import Flask, render_template

from database import db
from routes.auth_routes import auth_bp
from routes.dashboard_routes import dashboard_bp
from routes.files_routes import files_bp

app = Flask(__name__)

app.config["SECRET_KEY"] = "vaultsphere-secret-key"

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///vaultsphere.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False


db.init_app(app)


# Register blueprints
app.register_blueprint(auth_bp)
app.register_blueprint(dashboard_bp)


@app.route("/")
def home():
    return render_template("home.html")


with app.app_context():
    db.create_all()


if __name__ == "__main__":
    app.run(debug=True)