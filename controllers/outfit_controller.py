from flask import Blueprint, render_template, request, redirect, session, current_app, jsonify
from services.outfit_service import OutfitService
from services.clothing_service import ClothingService

#create blueprint for outfir routes
outfit_bp = Blueprint("outfit", __name__)


# handles all outfit-related routes and api endpoints
# requirements covered here: m7,m8,m9,s3,c1



# c1: view saved outfits with sorting filter
@outfit_bp.route("/saved-outfits")
def saved_outfits():
    #is user logged in? no, then redirect to login
    if not session.get("username"):
        return redirect("/login")
    # get sort parameter (default filter: newest first)
    sort = request.args.get("sort", "newest")
    #create outfitservice instance with db connection
    service = OutfitService(current_app.db)
    # fetch user outfits sorted by selected filter
    outfits = service.get_user_outfits(session.get("user_id"), sort=sort)

    #render template with outfits data and current sorting filter
    return render_template("saved_outfits.html", 
                         outfits=outfits, 
                         sort=sort,
                         active_page='saved-outfits')

#m7: api endpoint to save a new outfit
@outfit_bp.route("/api/save-outfit", methods=["POST"])
def save_outfit():
    #error if user not logged in
    if not session.get("user_id"):
        return jsonify({"error": "Not logged in"}), 401
    #get json data from request body
    data = request.get_json()

    #outfitservice instance created with db connection
    service = OutfitService(current_app.db)
    # save outfit with defaul "my outfit" if no name
    outfit_id = service.save_outfit(
        user_id=session.get("user_id"),
        outfit_name=data.get("outfit_name", "My Outfit"),
        top_id=data.get("top_id"),
        bottom_id=data.get("bottom_id"),
        footwear_id=data.get("footwear_id")
    )
    # return sucess response with new outfit ID
    return jsonify({"success": True, "outfit_id": outfit_id})

# m8 (update outfit) and s3 (renaming of outfits)
@outfit_bp.route("/api/update-outfit/<outfit_id>", methods=["PUT"])
def update_outfit(outfit_id):
    if not session.get("user_id"):
        return jsonify({"error": "Not logged in"}), 401
    #get json from request body
    data = request.get_json()

    service = OutfitService(current_app.db)
    # update clothing items and outfit if name provided
    service.update_outfit(
        outfit_id=outfit_id,
        outfit_name=data.get("outfit_name"),
        top_id=data.get("top_id"),
        bottom_id=data.get("bottom_id"),
        footwear_id=data.get("footwear_id")
    )
    #success
    return jsonify({"success": True})

# m9:delete saved outfit
@outfit_bp.route("/api/delete-outfit/<outfit_id>", methods=["DELETE"])
def delete_outfit(outfit_id):
    if not session.get("user_id"):
        #user logged in?
        return jsonify({"error": "Not logged in"}), 401

    # create instance with db connection
    service = OutfitService(current_app.db)
    #delete outfit from db
    service.delete_outfit(outfit_id)

    #success
    return jsonify({"success": True})

#m8: edit outfit page
@outfit_bp.route("/edit-outfit/<outfit_id>")
def edit_outfit(outfit_id):
    if not session.get("username"):
        return redirect("/login")
    # get service instances for db operations
    outfit_service = OutfitService(current_app.db)
    clothing_service = ClothingService(current_app.db)

    # get the outfit to edit by its ID
    outfit = outfit_service.get_outfit_by_id(outfit_id)
    # get all available clothing items for each category
    tops = clothing_service.get_by_category("top")
    bottoms = clothing_service.get_by_category("bottom")
    footwear = clothing_service.get_by_category("footwear")

    # render edit page with outfit data and all
    return render_template("edit_outfit.html",
                           outfit=outfit,
                           tops=tops,
                           bottoms=bottoms,
                           footwear=footwear,
                           active_page='saved-outfits')