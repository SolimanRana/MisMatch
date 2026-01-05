from flask import Blueprint, render_template, request, redirect, current_app, session, jsonify
from services.outfit_service import OutfitService

outfit_bp = Blueprint("outfit", __name__)

@outfit_bp.route("/save-outfit", methods=["POST"])
def save_outfit():
    """Save a new outfit"""
    if not session.get("user_id"):
        return jsonify({"error": "Not authenticated"}), 401
    
    try:
        data = request.get_json()
        top_id = data.get("top_id")
        bottom_id = data.get("bottom_id")
        footwear_id = data.get("footwear_id")
        outfit_name = data.get("outfit_name")  # Optional custom name
        
        # Validate that all items are provided
        if not all([top_id, bottom_id, footwear_id]):
            return jsonify({"error": "Please select all clothing items before saving"}), 400
        
        service = OutfitService(current_app.db)
        outfit = service.save_outfit(
            session["user_id"],
            top_id,
            bottom_id,
            footwear_id,
            outfit_name
        )
        
        return jsonify({
            "success": True,
            "message": f"{outfit['outfit_name']} saved successfully!",
            "outfit_id": str(outfit['_id'])
        }), 200
        
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": "Failed to save outfit"}), 500

@outfit_bp.route("/saved-outfits")
def saved_outfits():
    """Display all saved outfits"""
    if not session.get("user_id"):
        return redirect("/login")
    
    service = OutfitService(current_app.db)
    outfits = service.get_user_outfits_with_items(session["user_id"])
    
    return render_template("savedOutfits.html", outfits=outfits)

@outfit_bp.route("/delete-outfit/<outfit_id>", methods=["POST"])
def delete_outfit(outfit_id):
    """Delete a saved outfit"""
    if not session.get("user_id"):
        return jsonify({"error": "Not authenticated"}), 401
    
    try:
        service = OutfitService(current_app.db)
        service.delete_outfit(outfit_id, session["user_id"])
        
        return jsonify({
            "success": True,
            "message": "Outfit deleted successfully"
        }), 200
        
    except ValueError as e:
        return jsonify({"error": str(e)}), 404
    except Exception as e:
        return jsonify({"error": "Failed to delete outfit"}), 500