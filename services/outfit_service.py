from bson import ObjectId
from datetime import datetime

class OutfitService:
    def __init__(self, db):
        self.collection = db.outfits
        self.clothing = db.clothing

    def save_outfit(self, user_id, outfit_name, top_id, bottom_id, footwear_id):
        """Save a new outfit"""
        if not outfit_name or outfit_name.strip() == "" or outfit_name == "My Outfit":
          count = self.collection.count_documents({"user_id": user_id})
          outfit_name = f"My Outfit {count + 1}"  
        
        document = {
            "user_id": user_id,
            "outfit_name": outfit_name,
            "top_id": top_id,
            "bottom_id": bottom_id,
            "footwear_id": footwear_id,
            "created_at": datetime.utcnow()
        }
        result = self.collection.insert_one(document)
        return str(result.inserted_id)

    def get_user_outfits(self, user_id, sort="newest"):
        query = {"user_id": user_id}
        
        if sort == "newest":
            cursor = self.collection.find(query).sort("created_at", -1)
        elif sort == "oldest":
            cursor = self.collection.find(query).sort("created_at", 1)
        elif sort =="az":
            cursor = self.collection.find(query).sort("outfit_name", 1)
        else:
            cursor = self.collection.find(query)
            
        """Get all outfits for a user with clothing details"""
        outfits = list(cursor)

        for outfit in outfits:
            outfit['_id'] = str(outfit['_id'])
            # Get clothing details
            outfit['top'] = self.clothing.find_one({"_id": ObjectId(outfit['top_id'])})
            outfit['bottom'] = self.clothing.find_one({"_id": ObjectId(outfit['bottom_id'])})
            outfit['footwear'] = self.clothing.find_one({"_id": ObjectId(outfit['footwear_id'])})

        return outfits

    def get_outfit_by_id(self, outfit_id):
        """Get a single outfit by ID"""
        outfit = self.collection.find_one({"_id": ObjectId(outfit_id)})
        if outfit:
            outfit['_id'] = str(outfit['_id'])
        return outfit

    def update_outfit(self, outfit_id, outfit_name, top_id, bottom_id, footwear_id):
        """Update an existing outfit (FR-M8)"""
        self.collection.update_one(
            {"_id": ObjectId(outfit_id)},
            {"$set": {
                "outfit_name": outfit_name,
                "top_id": top_id,
                "bottom_id": bottom_id,
                "footwear_id": footwear_id,
                "updated_at": datetime.utcnow()
            }}
        )

    def delete_outfit(self, outfit_id):
        """Delete an outfit"""
        self.collection.delete_one({"_id": ObjectId(outfit_id)})