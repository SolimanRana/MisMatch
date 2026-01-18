from flask import Blueprint, render_template, session, redirect, current_app, jsonify
from services.clothing_service import ClothingService

generator_bp = Blueprint("generator", __name__)

# route to display the main dashboard with clothing items 
@generator_bp.route("/dashboard")
def dashboard():
    if not session.get("username"):
        return redirect("/login")
    
    service = ClothingService(current_app.db)
    
    # FR-M2: The app must use images of basic clothing items provided by the database
    # retrieve all items from DB by category
    tops = service.get_by_category("top")
    bottoms = service.get_by_category("bottom")
    footwear = service.get_by_category("footwear")
    
    # open dashboard/generator page
    return render_template("dashboard.html", 
                         tops=tops, 
                         bottoms=bottoms, 
                         footwear=footwear)