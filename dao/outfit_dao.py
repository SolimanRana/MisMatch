from datetime import datetime
from bson import ObjectId


# requirements: m7 (save outfits with default names)
#m8: edit saved outfit
#m9:delete saved fit
#s3: rename saved outfit

class OutfitDAO:
    #initialize DAO with db connection
    def __init__(self, db):
        #set collection reference to outfits collection
        self.collection = db.outfits

    # create new outfit in db
    def create_outfit(self, user_id, top_id, bottom_id, footwear_id, outfit_name=None):
        """Create a new outfit"""
        # generate outfit name if not provided
        if not outfit_name:
            #count existing outfits for user
            count = self.collection.count_documents({"user_id": user_id})
            #create default names like outfit 1,2..
            outfit_name = f"Outfit {count + 1}"

        #create outfit document with all required fields
        outfit_doc = {
            "user_id": user_id,
            "outfit_name": outfit_name,
            "top_id": top_id,
            "bottom_id": bottom_id,
            "footwear_id": footwear_id,
            "created_at": datetime.utcnow()
        }

        #insert document into db
        result = self.collection.insert_one(outfit_doc)
        #add generated id to document
        outfit_doc['_id'] = result.inserted_id
        #return complete outfit document
        return outfit_doc

    #get all outfits for specific user, starting with newest first
    def get_user_outfits(self, user_id):
        """Get all outfits for a specific user"""
        return list(self.collection.find({"user_id": user_id}).sort("created_at", -1))

    #get specific outfit by id for editing
    def get_outfit_by_id(self, outfit_id):
        """Get a specific outfit by ID"""
        return self.collection.find_one({"_id": ObjectId(outfit_id)})

    #delete an outfit from the db
    def delete_outfit(self, outfit_id, user_id):
        """Delete an outfit (only if it belongs to the user)"""
        result = self.collection.delete_one({
            "_id": ObjectId(outfit_id),
            "user_id": user_id
        })
        #return TRue if outfit was deleted, otherwise false
        return result.deleted_count > 0

    # rename outfit
    def update_outfit_name(self, outfit_id, user_id, new_name):
        """Update outfit name only if it belongs to user"""
        result = self.collection.update_one(
            {"_id": ObjectId(outfit_id), "user_id": user_id},
            {"$set": {"outfit_name": new_name}}
        )
        #return true if name was updated, otherwise false
        return result.modified_count > 0