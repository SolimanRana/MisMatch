from flask import Blueprint, render_template, session, redirect, current_app, jsonify
from services.clothing_service import ClothingService

generator_bp = Blueprint("generator", __name__)

@generator_bp.route("/dashboard")
def dashboard():
    if not session.get("username"):
        return redirect("/login")
    
    service = ClothingService(current_app.db)
    
    # retrieve all items
    tops = service.get_by_category("top")
    bottoms = service.get_by_category("bottom")
    footwear = service.get_by_category("footwear")
    
    return render_template("dashboard.html", 
                         tops=tops, 
                         bottoms=bottoms, 
                         footwear=footwear)