import os
from flask import Blueprint, request, jsonify, session, current_app
from werkzeug.utils import secure_filename
from datetime import datetime
from bson import ObjectId

upload_bp = Blueprint("upload", __name__)

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@upload_bp.route("/api/upload-clothing", methods=["POST"])
def upload_clothing():
    if not session.get("user_id"):
        return jsonify({"error": "Not logged in"}), 401

    if 'image' not in request.files:
        return jsonify({"error": "No image provided"}), 400

    file = request.files['image']
    category = request.form.get('category')

    if not category or category not in ['top', 'bottom', 'footwear']:
        return jsonify({"error": "Invalid category"}), 400

    if file.filename == '':
        return jsonify({"error": "No file selected"}), 400

    if file and allowed_file(file.filename):
        # Create unique filename
        filename = secure_filename(file.filename)
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        unique_filename = f"{session.get('user_id')}_{timestamp}_{filename}"

        # Save to uploads folder
        upload_folder = os.path.join(current_app.root_path, 'static', 'images', 'uploads')
        os.makedirs(upload_folder, exist_ok=True)

        filepath = os.path.join(upload_folder, unique_filename)
        file.save(filepath)

        # Save to database
        image_path = f"static/images/uploads/{unique_filename}"

        document = {
            "category": category,
            "subcategory": "custom",
            "subcategory_name": "custom_upload",
            "color": "custom",
            "neckline": None,
            "length": None,
            "image_path": image_path,
            "is_default": False,
            "user_id": session.get("user_id"),
            "created_at": datetime.utcnow()
        }

        result = current_app.db.clothing.insert_one(document)

        return jsonify({
            "success": True,
            "image_path": image_path,
            "item_id": str(result.inserted_id)
        })

    return jsonify({"error": "Invalid file type"}), 400