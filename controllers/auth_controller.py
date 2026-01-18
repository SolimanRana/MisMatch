from flask import Blueprint, render_template, request, redirect, current_app, session
from services.user_service import UserService

auth_bp = Blueprint("auth", __name__)

# FR-M3: The user must be able to create an account & login to the application
@auth_bp.route("/register", methods=["GET", "POST"])
def register_user():
    error = None

    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        password_repeat = request.form.get("password_repeat")

        # Validate that passwords match
        if password !=password_repeat:
            error = "Passwords don't match!"
            return render_template("register.html", error=error) 

        service = UserService(current_app.db)

        try:
            # create account
            user = service.register_user(username, password)

            # Store user session
            session["user_id"] = str(user["_id"])
            session["username"] = user["username"]
            session["avatar"] = user.get("avatar", "🙂")

            return redirect("/dashboard")
        except ValueError as e:
            error = str(e)
        
    return render_template("register.html", error=error)

# FR-M3: The user must be able to create an account & login to the application
@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    error = None

    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        service = UserService(current_app.db)

        try:
            # authenticate user login
            user = service.authenticate_user(username, password)

            # store user session
            session["user_id"] = str(user["_id"])
            session["username"] = user["username"]
            session["avatar"] = user.get("avatar", "🙂")

            return redirect("/dashboard")
        except ValueError as e:
            error = str(e)
        
    return render_template("index.html", error=error)

# FR-C3: The app could include a drop-down menu for user settings
# display settings page
@auth_bp.route("/settings")
def settings():
    if not session.get("username"):
        return redirect("/login")
    return render_template("settings.html")

# log out functionality
@auth_bp.route("/logout")
def logout():
    session.clear()
    return redirect("/")