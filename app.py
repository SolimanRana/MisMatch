from flask import Flask, render_template, session, redirect
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

    from controllers.generator_controller import generator_bp
    app.register_blueprint(generator_bp)

    from controllers.outfit_controller import outfit_bp
    app.register_blueprint(outfit_bp)

    from controllers.upload_controller import upload_bp
    app.register_blueprint(upload_bp)

    #Root Route
    @app.route("/")
    def index():
        if session.get("username"):
            return redirect("/dashboard")
        return render_template("index.html")
    
    @app.route("/dashboard")
    def dashboard():
        if not session.get("username"):
            return redirect("/login")
        return render_template("dashboard.html")

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)