class ClothingService:
    def __init__(self, db):
        self.collection = db.clothing

    def get_by_category(self, category):
        """
        retrieves all clothing items of each cetegory
        category: "top", "bottom", "footwear"
        """
        items = list(self.collection.find({"category": category}))
        
        # convert ObjectId to string for JSON
        for item in items:
            item['_id'] = str(item['_id'])
        
        return items

    def get_all_clothing(self):
        """retrieves all clothing items"""
        items = list(self.collection.find())
        
        # convert ObjectId to string for JSON
        for item in items:
            item['_id'] = str(item['_id'])
        
        return items