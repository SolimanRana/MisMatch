from flask import Blueprint, render_template, request, redirect, session, current_app
from services.user_service import UserService

settings_bp = Blueprint("settings", __name__)

# route to handle all user settings modifications
@settings_bp.route("/settings", methods=["GET", "POST"])
def settings():
    if not session.get("user_id"):
        return redirect("/login")

    service = UserService(current_app.db)
    error = None
    success = None
    
    if request.method == "POST":
        action = request.form.get("action")

        try:
            # FR-C5: The user could be able to choose their avatar (shown as the head of the character) from the given options. 
            if action == "change_avatar":
                avatar = request.form.get("avatar")
                if avatar:
                    service.change_avatar(session["user_id"], avatar)
                    session["avatar"] = avatar
                    success = "Avatar updated successfully"

            # FR-C4: The user could change their username...
            elif action == "change_username":
                new_username = request.form.get("new_username")
                service.change_username(session["user_id"], new_username)
                session["username"] = new_username
                success = "Username updated successfully"

            # FR-C4: ...and password using the edit button
            elif action == "change_password":
                old_pw = request.form.get("old_password")
                new_pw = request.form.get("new_password")
                service.change_password(session["user_id"], old_pw, new_pw)
                # log out after password change
                session.clear()
                return redirect("/login")

        except ValueError as e:
            error = str(e)

    # display settings page
    return render_template(
        "settings.html",
        avatar=session.get("avatar", "🙂"),
        error=error,
        success=success,
        active_page='settings'
    )