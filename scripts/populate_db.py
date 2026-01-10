"""
MisMatch Database Population Script
Populates MongoDB with clothing items from image files
"""

import os
import re
from pymongo import MongoClient
from datetime import datetime

# MongoDB connection
MONGODB_URI = "mongodb://localhost:27017/"  # Update if your MongoDB is hosted elsewhere
DATABASE_NAME = "mismatch"
COLLECTION_NAME = "clothing"

# Define subcategory mappings
TOPS_SUBCATEGORIES = {
    "1a": "oversized_tshirt",
    "1b": "slimfit_tshirt",
    "2": "longsleeve",
    "3": "sweatshirt",
    "4": "hoodie",
    "5": "shirt_blouse",
    "6": "tanktop",
    "7": "other"
}

BOTTOMS_SUBCATEGORIES = {
    "1": "jeans",
    "2": "dress_pants",
    "3": "jeans_skinny",
    "4": "leggings",
    "5": "skirt",
    "6": "shorts",
    "7": "sweatpants"
}

FOOTWEAR_SUBCATEGORIES = {
    "1": "sneakers"
}

def parse_filename(filename, category):
    """
    Parse filename to extract metadata
    
    Examples:
    - 1a_black_round.png -> subcategory=1a, color=black, neckline=round
    - 5_black_mini.png -> subcategory=5, color=black, length=mini
    - 1_white.png -> subcategory=1, color=white
    - default_tops.png -> is_default=True
    """
    
    # Remove file extension
    name = filename.replace('.png', '').replace('.jpg', '').replace('.jpeg', '')
    
    # Check if it's a default image
    if name.startswith('default_'):
        return {
            'subcategory': 'default',
            'subcategory_name': 'default',
            'color': None,
            'neckline': None,
            'length': None,
            'is_default': True
        }
    
    # Split by underscore
    parts = name.split('_')
    
    if len(parts) < 2:
        print(f"Warning: Could not parse filename: {filename}")
        return None
    
    subcategory = parts[0]
    color = parts[1] if len(parts) > 1 else None
    
    # Get subcategory name
    if category == 'top':
        subcategory_name = TOPS_SUBCATEGORIES.get(subcategory, 'unknown')
    elif category == 'bottom':
        subcategory_name = BOTTOMS_SUBCATEGORIES.get(subcategory, 'unknown')
    elif category == 'footwear':
        subcategory_name = FOOTWEAR_SUBCATEGORIES.get(subcategory, 'unknown')
    else:
        subcategory_name = 'unknown'
    
    # Check for neckline (for tops)
    neckline = None
    if len(parts) > 2 and parts[2] in ['round', 'v']:
        neckline = parts[2]
    
    # Check for length (for skirts)
    length = None
    if len(parts) > 2 and parts[2] in ['mini', 'long']:
        length = parts[2]
    
    return {
        'subcategory': subcategory,
        'subcategory_name': subcategory_name,
        'color': color,
        'neckline': neckline,
        'length': length,
        'is_default': False
    }

def create_clothing_document(filename, category, image_folder):
    """Create a MongoDB document for a clothing item"""
    
    metadata = parse_filename(filename, category)
    
    if metadata is None:
        return None
    
    # Construct image path (relative to static directory)
    # Updated to use clothing subfolder
    image_path = f"static/images/clothing/{image_folder}/{filename}"
    
    document = {
        'category': category,
        'subcategory': metadata['subcategory'],
        'subcategory_name': metadata['subcategory_name'],
        'color': metadata['color'],
        'neckline': metadata['neckline'],
        'length': metadata['length'],
        'image_path': image_path,
        'is_default': metadata['is_default'],
        'created_at': datetime.utcnow()
    }
    
    return document

def populate_database():
    """Main function to populate the database"""
    
    # Connect to MongoDB
    print("Connecting to MongoDB...")
    client = MongoClient(MONGODB_URI)
    db = client[DATABASE_NAME]
    collection = db[COLLECTION_NAME]
    
    # Clear existing data (optional - comment out if you want to keep existing data)
    print("Clearing existing clothing data...")
    collection.delete_many({})
    
    # Image data organized by category
    image_data = {
        'top': {
            'folder': 'tops',
            'files': [
                '1a_black_round.png',
                '1a_grey_round.png',
                '1a_marineblue_round.png',
                '1a_white_round.png',
                '1a_yellow_round.png',
                '1b_bordeaux_round.png',
                '1b_white_round.png',
                '2_beige_round.png',
                '2_black_round.png',
                '2_brown_round.png',
                '2_grey_round.png',
                '2_white_round.png',
                '3_black_round.png',
                '3_bordeaux_round.png',
                '3_brown_round.png',
                '3_green_round.png',
                '3_grey_round.png',
                '3_marineblue_round.png',
                '3_yellow_round.png',
                '6_black_v.png',
                '6_white_round.png',
                'default_tops.png',
            ]
        },
        'bottom': {
            'folder': 'bottoms',
            'files': [
                '1_black.png',
                '1_darkblue.png',
                '1_darkgray.png',
                '1_lightblue.png',
                '1_lightgray.png',
                '1_middleblue.png',
                '1_white.png',
                '2_beige.png',
                '2_black.png',
                '2_brown.png',
                '2_gray.png',
                '2_red.png',
                '4_black.png',
                '5_black_long.png',
                '5_black_mini.png',
                '5_bordeaux_long.png',
                '5_jeans_mini.png',
                '6_black.png',
                '6_gray.png',
                '6_grown.png',
                '6_lightblue.png',
                '6_middleblue.png',
                '7_black.png',
                '7_lightgray.png',
                'default_bottom.png',
            ]
        },
        'footwear': {
            'folder': 'footwear',
            'files': [
                '1_white.png',
                'default_footwear.png',
            ]
        }
    }
    
    # Insert documents
    total_inserted = 0
    
    for category, data in image_data.items():
        print(f"\nProcessing {category}s...")
        folder = data['folder']
        files = data['files']
        
        for filename in files:
            document = create_clothing_document(filename, category, folder)
            
            if document:
                result = collection.insert_one(document)
                print(f"  ✓ Inserted: {filename} (ID: {result.inserted_id})")
                total_inserted += 1
            else:
                print(f"  ✗ Skipped: {filename}")
    
    # Create indexes
    print("\nCreating indexes...")
    collection.create_index([("category", 1)])
    collection.create_index([("color", 1)])
    collection.create_index([("is_default", 1)])
    collection.create_index([("category", 1), ("color", 1)])
    print("  ✓ Indexes created")
    
    # Print summary
    print(f"\n{'='*50}")
    print(f"Database population complete!")
    print(f"Total items inserted: {total_inserted}")
    print(f"  - Tops: {collection.count_documents({'category': 'top'})}")
    print(f"  - Bottoms: {collection.count_documents({'category': 'bottom'})}")
    print(f"  - Footwear: {collection.count_documents({'category': 'footwear'})}")
    print(f"  - Default images: {collection.count_documents({'is_default': True})}")
    print(f"{'='*50}")
    
    # Close connection
    client.close()
    print("\nMongoDB connection closed.")

def verify_database():
    """Verify the database was populated correctly"""
    
    print("\n" + "="*50)
    print("VERIFICATION")
    print("="*50)
    
    client = MongoClient(MONGODB_URI)
    db = client[DATABASE_NAME]
    collection = db[COLLECTION_NAME]
    
    # Show some sample documents
    print("\nSample documents:")
    print("-" * 50)
    
    # One top
    top = collection.find_one({'category': 'top', 'is_default': False})
    if top:
        print(f"\n📦 TOPS Example:")
        print(f"  Subcategory: {top['subcategory_name']} ({top['subcategory']})")
        print(f"  Color: {top['color']}")
        print(f"  Neckline: {top['neckline']}")
        print(f"  Image: {top['image_path']}")
    
    # One bottom
    bottom = collection.find_one({'category': 'bottom', 'is_default': False})
    if bottom:
        print(f"\n👖 BOTTOMS Example:")
        print(f"  Subcategory: {bottom['subcategory_name']} ({bottom['subcategory']})")
        print(f"  Color: {bottom['color']}")
        print(f"  Length: {bottom['length']}")
        print(f"  Image: {bottom['image_path']}")
    
    # One footwear
    footwear = collection.find_one({'category': 'footwear', 'is_default': False})
    if footwear:
        print(f"\n👟 FOOTWEAR Example:")
        print(f"  Subcategory: {footwear['subcategory_name']} ({footwear['subcategory']})")
        print(f"  Color: {footwear['color']}")
        print(f"  Image: {footwear['image_path']}")
    
    # Default images
    print(f"\n❓ DEFAULT IMAGES:")
    defaults = collection.find({'is_default': True})
    for default in defaults:
        print(f"  - {default['category']}: {default['image_path']}")
    
    # Color distribution
    print(f"\n🎨 COLOR DISTRIBUTION:")
    colors = collection.distinct('color', {'is_default': False})
    colors = [c for c in colors if c is not None]
    print(f"  Available colors: {', '.join(sorted(colors))}")
    colors = collection.distinct('color', {'is_default': False})
    colors = [c for c in colors if c is not None]
    print(f"  Available colors: {', '.join(sorted(colors))}")
    
    client.close()
    print("\n" + "="*50)

if __name__ == "__main__":
    print("="*50)
    print("MisMatch Database Population Script")
    print("="*50)
    
    try:
        populate_database()
        verify_database()
        
        print("\n✅ SUCCESS! Your database is ready to use.")
        print("\nNext steps:")
        print("1. Run your Flask application")
        print("2. Test the outfit generation features")
        
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        print("\nPlease check:")
        print("1. MongoDB is running")
        print("2. MongoDB connection string is correct")
        print("3. You have pymongo installed: pip install pymongo")
        print("4. Your images are in: static/images/clothing/tops/, bottoms/, footwear/")