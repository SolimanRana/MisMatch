from flask import Flask, render_template, session, redirect
from pymongo import MongoClient
from controllers.wardrobe_controller import wardrobe_bp

def create_app():
    # FR-M1: The app must be accessible as a web application (Flask)
    app = Flask(__name__)
    app.secret_key = "dev-secret"

    # FR-M2: The app must use images of basic clothing items provided by the database (MongoDB connection)
    client = MongoClient("mongodb://localhost:27017")
    app.db = client["mismatch"]

    # FR-M3: The user must be able to create an account & login to the application
    # auth_bp provides registration & login routes
    from controllers.auth_controller import auth_bp
    app.register_blueprint(auth_bp) 

    # generator_bp provides dashboard with clothing display functionality
    from controllers.generator_controller import generator_bp
    app.register_blueprint(generator_bp)

    # outfit_bp handles saving, editing, deleting & filtering outfits
    from controllers.outfit_controller import outfit_bp
    app.register_blueprint(outfit_bp)

    # upload_bp handles uploading custom clothing items
    from controllers.upload_controller import upload_bp
    app.register_blueprint(upload_bp)
    
    # settings_bp provides user settings functionality
    from controllers.settings_controller import settings_bp
    app.register_blueprint(settings_bp)
    
    # wardrobe_bp provides category based filtering (top, bottom, footwear) 
    from controllers.wardrobe_controller import wardrobe_bp
    app.register_blueprint(wardrobe_bp)

    # Root Route
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