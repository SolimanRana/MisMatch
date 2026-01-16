from flask import Blueprint, render_template, request, redirect, session, current_app, jsonify
from services.outfit_service import OutfitService
from services.clothing_service import ClothingService

outfit_bp = Blueprint("outfit", __name__)

@outfit_bp.route("/saved-outfits")
def saved_outfits():
    if not session.get("username"):
        return redirect("/login")
    
    sort = request.args.get("sort", "newest")

    service = OutfitService(current_app.db)
    outfits = service.get_user_outfits(session.get("user_id"), sort=sort)

    return render_template("saved_outfits.html", 
                         outfits=outfits, 
                         sort=sort,
                         active_page='saved-outfits')

@outfit_bp.route("/api/save-outfit", methods=["POST"])
def save_outfit():
    if not session.get("user_id"):
        return jsonify({"error": "Not logged in"}), 401

    data = request.get_json()

    service = OutfitService(current_app.db)
    outfit_id = service.save_outfit(
        user_id=session.get("user_id"),
        outfit_name=data.get("outfit_name", "My Outfit"),
        top_id=data.get("top_id"),
        bottom_id=data.get("bottom_id"),
        footwear_id=data.get("footwear_id")
    )

    return jsonify({"success": True, "outfit_id": outfit_id})

@outfit_bp.route("/api/update-outfit/<outfit_id>", methods=["PUT"])
def update_outfit(outfit_id):
    if not session.get("user_id"):
        return jsonify({"error": "Not logged in"}), 401

    data = request.get_json()

    service = OutfitService(current_app.db)
    service.update_outfit(
        outfit_id=outfit_id,
        outfit_name=data.get("outfit_name"),
        top_id=data.get("top_id"),
        bottom_id=data.get("bottom_id"),
        footwear_id=data.get("footwear_id")
    )

    return jsonify({"success": True})

@outfit_bp.route("/api/delete-outfit/<outfit_id>", methods=["DELETE"])
def delete_outfit(outfit_id):
    if not session.get("user_id"):
        return jsonify({"error": "Not logged in"}), 401

    service = OutfitService(current_app.db)
    service.delete_outfit(outfit_id)

    return jsonify({"success": True})

@outfit_bp.route("/edit-outfit/<outfit_id>")
def edit_outfit(outfit_id):
    if not session.get("username"):
        return redirect("/login")

    outfit_service = OutfitService(current_app.db)
    clothing_service = ClothingService(current_app.db)

    outfit = outfit_service.get_outfit_by_id(outfit_id)
    tops = clothing_service.get_by_category("top")
    bottoms = clothing_service.get_by_category("bottom")
    footwear = clothing_service.get_by_category("footwear")

    return render_template("edit_outfit.html",
                           outfit=outfit,
                           tops=tops,
                           bottoms=bottoms,
                           footwear=footwear,
                           active_page='saved-outfits')