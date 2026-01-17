from flask import Blueprint, render_template, current_app
from services.clothing_service import ClothingService

wardrobe_bp = Blueprint("wardrobe", __name__)

@wardrobe_bp.route("/wardrobe/<category>")
def wardrobe_category(category):
    service = ClothingService(current_app.db)
    
    if category not in ['top', 'bottom', 'footwear']:
        return "Category not found", 404
    
    items = service.get_by_category(category) #get all items by category
    return render_template("wardrobe.html", items=items, category=category)