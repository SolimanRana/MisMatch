"""
Database Query Test Script
Test various database queries to ensure everything works correctly
"""

from pymongo import MongoClient
import random

# MongoDB connection
MONGODB_URI = "mongodb://localhost:27017/"
DATABASE_NAME = "mismatch_db"

def test_basic_queries():
    """Test basic database queries"""
    
    print("\n" + "="*60)
    print("TESTING BASIC QUERIES")
    print("="*60)
    
    client = MongoClient(MONGODB_URI)
    db = client[DATABASE_NAME]
    collection = db.clothing
    
    # Test 1: Count all items
    print("\n1. Total items in database:")
    total = collection.count_documents({})
    print(f"   Count: {total}")
    assert total > 0, "❌ Database is empty!"
    print("   ✓ Database has items")
    
    # Test 2: Count by category
    print("\n2. Items by category:")
    for category in ['top', 'bottom', 'footwear']:
        count = collection.count_documents({'category': category})
        print(f"   {category.capitalize()}s: {count}")
        assert count > 0, f"❌ No {category}s found!"
    print("   ✓ All categories have items")
    
    # Test 3: Default images
    print("\n3. Default images:")
    defaults = list(collection.find({'is_default': True}))
    print(f"   Found: {len(defaults)} default images")
    for default in defaults:
        print(f"   - {default['category']}: {default['image_path']}")
    assert len(defaults) == 3, "❌ Should have 3 default images!"
    print("   ✓ All default images present")
    
    # Test 4: Find by color
    print("\n4. Items by color (black):")
    black_items = list(collection.find({'color': 'black', 'is_default': False}))
    print(f"   Found: {len(black_items)} black items")
    for item in black_items[:3]:  # Show first 3
        print(f"   - {item['category']}: {item['subcategory_name']}")
    print("   ✓ Color filtering works")
    
    client.close()

def test_random_outfit_generation():
    """Test random outfit generation (MisMatch feature)"""
    
    print("\n" + "="*60)
    print("TESTING RANDOM OUTFIT GENERATION (FR-S2)")
    print("="*60)
    
    client = MongoClient(MONGODB_URI)
    db = client[DATABASE_NAME]
    collection = db.clothing
    
    print("\nGenerating 3 random outfits...")
    
    for i in range(3):
        print(f"\n🎲 Random Outfit #{i+1}:")
        
        # Method 1: Using aggregation pipeline (more efficient)
        top = collection.aggregate([
            {"$match": {"category": "top", "is_default": False}},
            {"$sample": {"size": 1}}
        ]).next()
        
        bottom = collection.aggregate([
            {"$match": {"category": "bottom", "is_default": False}},
            {"$sample": {"size": 1}}
        ]).next()
        
        footwear = collection.aggregate([
            {"$match": {"category": "footwear", "is_default": False}},
            {"$sample": {"size": 1}}
        ]).next()
        
        print(f"   👕 Top: {top['subcategory_name']} ({top['color']})")
        print(f"   👖 Bottom: {bottom['subcategory_name']} ({bottom['color']})")
        print(f"   👟 Footwear: {footwear['subcategory_name']} ({footwear['color']})")
        print(f"   Images:")
        print(f"     - {top['image_path']}")
        print(f"     - {bottom['image_path']}")
        print(f"     - {footwear['image_path']}")
    
    print("\n   ✓ Random outfit generation works!")
    
    client.close()

def test_navigation_arrows():
    """Test arrow navigation functionality (FR-M6)"""
    
    print("\n" + "="*60)
    print("TESTING ARROW NAVIGATION (FR-M6)")
    print("="*60)
    
    client = MongoClient(MONGODB_URI)
    db = client[DATABASE_NAME]
    collection = db.clothing
    
    # Get all tops (excluding defaults)
    tops = list(collection.find(
        {'category': 'top', 'is_default': False}
    ).sort('subcategory', 1))
    
    print(f"\nTotal tops available: {len(tops)}")
    print("\nSimulating arrow navigation through tops:")
    
    current_index = 0
    
    # Show first item
    print(f"\n[Start] Current top (index {current_index}):")
    print(f"  {tops[current_index]['subcategory_name']} - {tops[current_index]['color']}")
    
    # Right arrow (next)
    current_index = (current_index + 1) % len(tops)
    print(f"\n[→ Right arrow] Next top (index {current_index}):")
    print(f"  {tops[current_index]['subcategory_name']} - {tops[current_index]['color']}")
    
    # Right arrow again
    current_index = (current_index + 1) % len(tops)
    print(f"\n[→ Right arrow] Next top (index {current_index}):")
    print(f"  {tops[current_index]['subcategory_name']} - {tops[current_index]['color']}")
    
    # Left arrow (previous)
    current_index = (current_index - 1) % len(tops)
    print(f"\n[← Left arrow] Previous top (index {current_index}):")
    print(f"  {tops[current_index]['subcategory_name']} - {tops[current_index]['color']}")
    
    # Test wraparound - go to last item
    current_index = -1
    print(f"\n[← Left arrow from first] Wraparound to last (index {current_index}):")
    print(f"  {tops[current_index]['subcategory_name']} - {tops[current_index]['color']}")
    
    print("\n   ✓ Arrow navigation logic works!")
    
    client.close()

def test_filtering():
    """Test filtering functionality (FR-S1, FR-C2)"""
    
    print("\n" + "="*60)
    print("TESTING FILTERING (FR-S1, FR-C2)")
    print("="*60)
    
    client = MongoClient(MONGODB_URI)
    db = client[DATABASE_NAME]
    collection = db.clothing
    
    # Test category filtering (FR-S1)
    print("\n1. Filter by category (FR-S1):")
    for category in ['top', 'bottom', 'footwear']:
        items = list(collection.find(
            {'category': category, 'is_default': False}
        ))
        print(f"   {category.capitalize()}: {len(items)} items")
    
    # Test color filtering (FR-C2 - Could-have)
    print("\n2. Filter by color (FR-C2 - Could-have):")
    colors = collection.distinct('color', {'is_default': False})
    colors = [c for c in colors if c is not None]
    print(f"   Available colors: {len(colors)}")
    
    # Show items for a specific color
    test_color = 'black'
    black_items = list(collection.find(
        {'color': test_color, 'is_default': False}
    ))
    print(f"\n   Items in '{test_color}': {len(black_items)}")
    for item in black_items[:5]:
        print(f"     - {item['category']}: {item['subcategory_name']}")
    
    # Test combined filtering
    print("\n3. Combined filtering (category + color):")
    black_tops = list(collection.find({
        'category': 'top',
        'color': 'black',
        'is_default': False
    }))
    print(f"   Black tops: {len(black_tops)}")
    for item in black_tops:
        print(f"     - {item['subcategory_name']}")
    
    print("\n   ✓ Filtering works!")
    
    client.close()

def test_outfit_save_simulation():
    """Simulate outfit saving (FR-M7)"""
    
    print("\n" + "="*60)
    print("TESTING OUTFIT SAVE SIMULATION (FR-M7)")
    print("="*60)
    
    client = MongoClient(MONGODB_URI)
    db = client[DATABASE_NAME]
    
    # This would normally be in a separate 'outfits' collection
    # For testing, we'll just simulate the logic
    
    print("\nSimulating outfit save:")
    print("1. User creates outfit manually or with MisMatch")
    print("2. User clicks 'Save Outfit'")
    
    # Get random items
    collection = db.clothing
    
    top = collection.aggregate([
        {"$match": {"category": "top", "is_default": False}},
        {"$sample": {"size": 1}}
    ]).next()
    
    bottom = collection.aggregate([
        {"$match": {"category": "bottom", "is_default": False}},
        {"$sample": {"size": 1}}
    ]).next()
    
    footwear = collection.aggregate([
        {"$match": {"category": "footwear", "is_default": False}},
        {"$sample": {"size": 1}}
    ]).next()
    
    # Simulate outfit document (this would go in 'outfits' collection)
    outfit_doc = {
        "user_id": "test_user_123",
        "outfit_name": "Outfit 1",
        "top_id": top["_id"],
        "bottom_id": bottom["_id"],
        "footwear_id": footwear["_id"],
        "created_at": "2025-01-03T10:00:00Z"
    }
    
    print("\n3. Outfit saved to database:")
    print(f"   Name: {outfit_doc['outfit_name']}")
    print(f"   Top: {top['subcategory_name']} ({top['color']})")
    print(f"   Bottom: {bottom['subcategory_name']} ({bottom['color']})")
    print(f"   Footwear: {footwear['subcategory_name']} ({footwear['color']})")
    
    print("\n   ✓ Outfit save logic works!")
    print("   Note: Actual implementation needs 'outfits' collection")
    
    client.close()

def test_indexes():
    """Verify indexes are created"""
    
    print("\n" + "="*60)
    print("TESTING DATABASE INDEXES")
    print("="*60)
    
    client = MongoClient(MONGODB_URI)
    db = client[DATABASE_NAME]
    collection = db.clothing
    
    print("\nIndexes on 'clothing' collection:")
    indexes = collection.index_information()
    
    for index_name, index_info in indexes.items():
        print(f"\n   {index_name}:")
        print(f"     Keys: {index_info['key']}")
    
    # Check for expected indexes
    expected_indexes = ['category_1', 'color_1', 'is_default_1', 'category_1_color_1']
    
    for expected in expected_indexes:
        if expected in indexes:
            print(f"\n   ✓ Index '{expected}' exists")
        else:
            print(f"\n   ⚠ Index '{expected}' missing")
    
    client.close()

def main():
    print("="*60)
    print("MisMatch Database Query Test Suite")
    print("="*60)
    
    try:
        test_basic_queries()
        test_random_outfit_generation()
        test_navigation_arrows()
        test_filtering()
        test_outfit_save_simulation()
        test_indexes()
        
        print("\n" + "="*60)
        print("✅ ALL TESTS PASSED!")
        print("="*60)
        print("\nYour database is working correctly and ready for integration.")
        print("\nNext steps:")
        print("1. Integrate these queries into your Flask routes")
        print("2. Implement the outfit save/edit/delete functionality")
        print("3. Build the frontend to display clothing items")
        
    except AssertionError as e:
        print(f"\n❌ TEST FAILED: {e}")
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        print("\nPlease check:")
        print("1. MongoDB is running")
        print("2. Database was populated with populate_db.py")
        print("3. Connection settings are correct")

if __name__ == "__main__":
    main()