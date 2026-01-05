from dao.outfit_dao import OutfitDAO
from bson import ObjectId

class OutfitService:
    def __init__(self, db):
        self.outfit_dao = OutfitDAO(db)
        self.clothing_collection = db.clothing

    def save_outfit(self, user_id, top_id, bottom_id, footwear_id, outfit_name=None):
        """Save a new outfit"""
        # Validate that all clothing items exist
        if not self._validate_clothing_item(top_id):
            raise ValueError("Invalid top item")
        if not self._validate_clothing_item(bottom_id):
            raise ValueError("Invalid bottom item")
        if not self._validate_clothing_item(footwear_id):
            raise ValueError("Invalid footwear item")
        
        # Create outfit
        outfit = self.outfit_dao.create_outfit(user_id, top_id, bottom_id, footwear_id, outfit_name)
        return outfit

    def get_user_outfits_with_items(self, user_id):
        """Get all outfits for a user with clothing item details"""
        outfits = self.outfit_dao.get_user_outfits(user_id)
        
        # Populate each outfit with clothing item details
        for outfit in outfits:
            outfit['_id'] = str(outfit['_id'])
            outfit['top'] = self.clothing_collection.find_one({"_id": ObjectId(outfit['top_id'])})
            outfit['bottom'] = self.clothing_collection.find_one({"_id": ObjectId(outfit['bottom_id'])})
            outfit['footwear'] = self.clothing_collection.find_one({"_id": ObjectId(outfit['footwear_id'])})
        
        return outfits

    def delete_outfit(self, outfit_id, user_id):
        """Delete an outfit"""
        success = self.outfit_dao.delete_outfit(outfit_id, user_id)
        if not success:
            raise ValueError("Outfit not found or you don't have permission to delete it")
        return True

    def _validate_clothing_item(self, item_id):
        """Validate that a clothing item exists"""
        try:
            item = self.clothing_collection.find_one({"_id": ObjectId(item_id)})
            return item is not None
        except:
            return False