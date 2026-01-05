from datetime import datetime
from bson import ObjectId

class OutfitDAO:
    def __init__(self, db):
        self.collection = db.outfits

    def create_outfit(self, user_id, top_id, bottom_id, footwear_id, outfit_name=None):
        """Create a new outfit"""
        # Generate outfit name if not provided
        if not outfit_name:
            count = self.collection.count_documents({"user_id": user_id})
            outfit_name = f"Outfit {count + 1}"
        
        outfit_doc = {
            "user_id": user_id,
            "outfit_name": outfit_name,
            "top_id": top_id,
            "bottom_id": bottom_id,
            "footwear_id": footwear_id,
            "created_at": datetime.utcnow()
        }
        
        result = self.collection.insert_one(outfit_doc)
        outfit_doc['_id'] = result.inserted_id
        return outfit_doc

    def get_user_outfits(self, user_id):
        """Get all outfits for a specific user"""
        return list(self.collection.find({"user_id": user_id}).sort("created_at", -1))

    def get_outfit_by_id(self, outfit_id):
        """Get a specific outfit by ID"""
        return self.collection.find_one({"_id": ObjectId(outfit_id)})

    def delete_outfit(self, outfit_id, user_id):
        """Delete an outfit (only if it belongs to the user)"""
        result = self.collection.delete_one({
            "_id": ObjectId(outfit_id),
            "user_id": user_id
        })
        return result.deleted_count > 0

    def update_outfit_name(self, outfit_id, user_id, new_name):
        """Update outfit name"""
        result = self.collection.update_one(
            {"_id": ObjectId(outfit_id), "user_id": user_id},
            {"$set": {"outfit_name": new_name}}
        )
        return result.modified_count > 0