from flask import Flask, render_template
from pymongo import MongoClient

def create_app():
    app = Flask(__name__)
    app.secret_key = "dev-secret"

    #MongoDB
    client = MongoClient("mongodb://localhost:27017")
    app.db = client["mismatch"]

    #Blueprints
    from controllers.auth_controller import auth_bp
    app.register_blueprint(auth_bp)

    #Root Route
    @app.route("/")
    def index():
        return render_template("index.html")

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
