from flask import Blueprint, render_template, current_app
from services.clothing_service import ClothingService

wardrobe_bp = Blueprint("wardrobe", __name__)

# FR-S1: The user should be able to filter the clothing using a “hamburger menu” which consists of the following sorting options: top, bottom and footwear
@wardrobe_bp.route("/wardrobe/<category>")
def wardrobe_category(category):
    service = ClothingService(current_app.db)
    
    if category not in ['top', 'bottom', 'footwear']:
        return "Category not found", 404
    
    # get all items by selected category
    # retrieve clothing items from db
    items = service.get_by_category(category) 
    return render_template("wardrobe.html", items=items, category=category)