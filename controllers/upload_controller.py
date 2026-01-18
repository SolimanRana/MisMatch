import os
from flask import Blueprint, request, jsonify, session, current_app
from werkzeug.utils import secure_filename
from datetime import datetime
from bson import ObjectId


#s4: upload feature for uses to add their own clothes

#blueprint
upload_bp = Blueprint("upload", __name__)


# allowed file extensions for image upload
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

# helper function to check if file format is allowed
def allowed_file(filename):
    # check if filename has format and if it is allowed
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# api endpoint to upload custom clothes
@upload_bp.route("/api/upload-clothing", methods=["POST"])
def upload_clothing():
    # user logged in?
    if not session.get("user_id"):
        return jsonify({"error": "Not logged in"}), 401

    # error if no image file in request
    if 'image' not in request.files:
        return jsonify({"error": "No image provided"}), 400
    # get uploaded file and category from request
    file = request.files['image']
    category = request.form.get('category')

    #error if category wrong
    if not category or category not in ['top', 'bottom', 'footwear']:
        return jsonify({"error": "Invalid category"}), 400
    #error if no file selected
    if file.filename == '':
        return jsonify({"error": "No file selected"}), 400

    # process and save uploaded file
    if file and allowed_file(file.filename):
        # Create unique filename and timestamp
        filename = secure_filename(file.filename)
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        # unique filename with user id and timestamp
        unique_filename = f"{session.get('user_id')}_{timestamp}_{filename}"

        # Save to uploads folder
        upload_folder = os.path.join(current_app.root_path, 'static', 'images', 'uploads')
        # create folder if no exists
        os.makedirs(upload_folder, exist_ok=True)

        # create full timepath and save file
        filepath = os.path.join(upload_folder, unique_filename)
        file.save(filepath)

        # Save to database
        image_path = f"static/images/uploads/{unique_filename}"

        #create document for mongoDB with clothing item data
        document = {
            "category": category,
            "subcategory": "custom",
            "subcategory_name": "custom_upload",
            "color": "custom",
            "neckline": None,
            "length": None,
            "image_path": image_path, # path to saved image
            "is_default": False, # not default item
            "user_id": session.get("user_id"), # link to user who uploaded
            "created_at": datetime.utcnow() #timestamp
        }

        # insert document into clothing collection
        result = current_app.db.clothing.insert_one(document)

        #success response with image path and item
        return jsonify({
            "success": True,
            "image_path": image_path,
            "item_id": str(result.inserted_id)
        })
    #error if file type wrong
    return jsonify({"error": "Invalid file type"}), 400

#api endpoint to delete custom upload
@upload_bp.route("/api/delete-clothing/<item_id>", methods=["DELETE"])
def delete_clothing(item_id):
    if not session.get("user_id"):
        #user logged in?
        return jsonify({"error": "Not logged in"}), 401

    # imprt objectid for mongo db query
    from bson import ObjectId

    # delete only the users own uploads
    result = current_app.db.clothing.delete_one({
        "_id": ObjectId(item_id),
        "user_id": session.get("user_id")
    })

    #success when deleted
    if result.deleted_count > 0:
        return jsonify({"success": True})
    #return error if item not the users or not found
    else:
        return jsonify({"error": "Item not found or not yours"}), 404