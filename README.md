# MisMatch

A web-based virtual wardrobe application that helps users visualize outfit combinations. Users can browse through clothing items, create outfit combinations, and save their favorite looks. The application also supports uploading custom clothing items.

## MoSCoW Requirements

### Must-Have Criteria (FR-M)

- **FR-M1**: The app must be accessible as a web application
- **FR-M2**: The app must use images of basic clothing items provided by the database
- **FR-M3**: The user must be able to create an account and log in to the application
- **FR-M4**: The app must start with a default screen containing question marks "?" instead of clothing items
- **FR-M5**: The user must be able to see boxes displaying clothing items as images (tops, bottoms, footwear)
- **FR-M6**: The user must be able to move from one item to another using arrow buttons
- **FR-M7**: The user must be able to save outfits with default names (e.g., "Outfit 1")
- **FR-M8**: The user must be able to edit saved outfits
- **FR-M9**: The user must be able to delete saved outfits

### Should-Have Criteria (FR-S)

- **FR-S1**: The user should be able to filter clothing using a hamburger menu (top, bottom, footwear)
- **FR-S2**: The user should be able to use a "MisMatch" button to create random outfit combinations
- **FR-S3**: The user should be able to rename saved outfits
- **FR-S4**: The app should include an upload feature for users to add their own clothing items

### Could-Have Criteria (FR-C)

- **FR-C1**: The user could be able to filter saved outfits (newest first, oldest first, a-z)
- **FR-C2**: The user could be able to filter clothing items by color
- **FR-C3**: The app could include a drop-down menu for user settings
- **FR-C4**: The user could change their username and password
- **FR-C5**: The user could be able to choose their avatar from given options

### Won't-Have Criteria (FR-W)

- **FR-W1**: The user will not be able to rate outfits
- **FR-W2**: The user will not be able to like/dislike items
- **FR-W3**: The app will not include an AI assistant
- **FR-W4**: The app will not include one-piece items such as dresses, overalls, onesies, etc.

## Setup Instructions

### Prerequisites

- Python 3.8 or higher
- MongoDB Community Edition
- MongoDB Compass

### MongoDB Installation

1. Go to https://www.mongodb.com/try/download/community
2. Install as a service
3. Run service as a network service
4. Click Next/Install
5. Also download MongoDB Compass (database GUI)

### MongoDB Compass Setup

1. Open MongoDB Compass and create a new connection:
   - **URI**: `mongodb://localhost:27017`
   - **Name**: MisMatch
   - **Color**: (optional, choose any color you like)
2. Click "Save & Connect"

### Create Username Index

To prevent duplicate usernames:

1. In MongoDB Compass, navigate to the `users` collection
2. Click on the **INDEXES** tab
3. Click **Create Index**
4. Configure:
   - **Field**: `username`
   - **Order**: Ascending (1)
   - **Check**: unique (check this box)
5. Click "Create"

You should now see:
- `users` collection with usernames and hashed passwords (and `createdAt` timestamps)
- `clothing` collection with all clothing items
- `outfits` collection (created when users save outfits)

### Installation

1. Clone the repository
2. Create a virtual environment
3. Install dependencies
4. Populate the database
5. Run the application

### Daily Workflow (for Developers)
```bash
# 1. Activate virtual environment
source venv/bin/activate          # macOS/Linux
.\venv\Scripts\activate            # Windows

# 2. Pull latest changes
git pull origin main

# 3. If requirements.txt changed, reinstall dependencies
pip install -r requirements.txt

# 4. If you added new clothing items, re-run populate script
python scripts/populate_db.py

# 5. Run the application
python app.py
```

The application will start at: http://127.0.0.1:5000

Open your web browser and navigate to this URL.

## How to Use

### 1. Create an Account

- Open the application in your browser
- Click on "Register Now"
- Enter a username and password
- Click "Sign Up"

### 2. Login

- On the homepage, click "Login"
- Enter your credentials
- You'll be redirected to the dashboard

### 3. Browse Clothing Items

- The dashboard displays three boxes: TOPS, BOTTOMS, and FOOTWEAR
- Initially, each box shows a "?" placeholder
- Click the arrow buttons (◀ ▶) next to each box to browse through available items
- Clothing images from the database will appear in the boxes

### 4. Generate Random Outfits

- Click the "MisMatch" button at the bottom
- The app will randomly select one item from each category
- Continue clicking to generate new random combinations

### 5. Filter Clothing

**By Category (Hamburger Menu)**:
- Click the hamburger menu (☰) in the top right
- Select Tops, Bottoms, or Footwear to view all items in that category

**By Color**:
- Click the "Filter" button below any clothing box
- Select a color from the dropdown menu
- Click on an item in the grid to display it

### 6. Save an Outfit

- Browse or generate an outfit you like
- Click the "Save Outfit" button
- Enter a name for your outfit (or use the default name)
- Click OK

### 7. View Saved Outfits

- Click "Saved Outfits" in the navigation bar
- You'll see all your saved outfits with their names and images
- Use the "Sort by" dropdown to organize outfits (newest, oldest, a-z)

### 8. Edit a Saved Outfit

- Go to "Saved Outfits"
- Click the "Edit" button on any outfit
- Use the arrow buttons to change clothing items
- Edit the outfit name if desired
- Click "Save Changes"

### 9. Delete a Saved Outfit

- Go to "Saved Outfits"
- Click the "Delete" button on the outfit you want to remove
- Confirm the deletion

### 10. Upload Your Own Clothing

- On the dashboard, click the "Upload" button
- Select a category (Top, Bottom, or Footwear)
- Choose an image file (PNG, JPG, or JPEG)
- Click "Upload"
- Refresh the page to see your uploaded item

### 11. Manage User Settings

- Click your username in the top right corner
- Select "Settings" from the dropdown menu

**In Settings, you can**:
- **Change Username**: Enter a new username and click "Update Username"
- **Change Password**: Enter your old password and new password, then click "Update Password"
- **Choose Avatar**: Select an emoji avatar and click "Save Avatar"

### 12. Logout

- Click your username in the top right corner
- Select "Logout" from the dropdown menu

## Clothing Categories Reference
Used to categorise the clothing items in the database, just for devs.
### TOPS
- 1a = Oversized/regular t-shirts
- 1b = Slim-fit t-shirts
- 2 = Long sleeves
- 3 = Sweatshirt
- 4 = Hoodie
- 5 = Shirt/blouse
- 6 = Tank tops
- 7 = Other

### BOTTOMS
- 1 = Jeans
- 2 = Dress pants
- 3 = Skinny jeans
- 4 = Leggings
- 5 = Skirts
- 6 = Shorts
- 7 = Sweatpants

### SHOES
- 1 = Sneaker
- 2 = Loafer/ Mules
- 3 = Heels
- 4 = Boots

