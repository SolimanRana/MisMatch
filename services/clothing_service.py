
#requirements
#m2: use images of basic clothing items provided
#m5: display clothing items as images


class ClothingService:
    #initalize service with db connection
    def __init__(self, db):
        # set collection refernce to clothing collection
        self.collection = db.clothing

    #get all clothing items for a specific category
    def get_by_category(self, category):
        """
        retrieves all clothing items of each cetegory
        category: "top", "bottom", "footwear"
        """
        items = list(self.collection.find({"category": category}))
        
        # convert ObjectId to string for JSON
        for item in items:
            item['_id'] = str(item['_id'])
        #return list of clothes
        return items

    def get_all_clothing(self):
        """retrieves all clothing items"""
        items = list(self.collection.find())
        
        # convert ObjectId to string for JSON
        for item in items:
            item['_id'] = str(item['_id'])
        #returns list of all clothing items
        return items