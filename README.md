This is the repository for our Software Engineering Project "MisMatch", a web based virtual wardrobe application that helps users visualize outfit combinations. 


Setup Instructions
Clone the repo and create virtual env, install dependecies, install and start MongoDB, populate the database, verify setup, run the application

How to install and start MongoDB:
Go to https://www.mongodb.com/try/download/community 
install as a service
run service as a network service
then click next/install

!! Also download MongoDB Compass (database GUI)

MongoDB Compass Setup
Open MongoDB Compass and create a new connection:
    **URI**: `mongodb://localhost:27017`
    **Name**: MisMatch
    **Color**: (optional, choose any color you like)
Click Save & Connect

Create Username Index to prevent duplicate usernames:

In MongoDB Compass, navigate to the `users` collection. 
Click on **INDEXES** tab
Click **Create Index**
Configure:
    **Field**: `username`
    **Order**: Ascending (1)
    **Check**: unique (check this box)
Click create

Now you should see:
users collection with usernames and hashed passwords (and `createdAt` timestamps)
clothing collection with all clothing items
outfits collection (created when users save outfits)

-------------------

NEUES TERMINAL ALS ADMIN AUSFÜHREN (am PC selbst ich habe PowerShell verwendet):
net start MongoDB

um zu überprüfen ob mongoDB läuft:
Get-Service MongoDB -> da sollte dann irgendwo running stehen.

im Terminal (ich arbeite mit Visual Studio Code: windows shortcut: strg + ö):
py -m venv venv
ODER
python -m venv venv
(2 Optionen falls eines von den beiden error code schlägt)

.\venv\Scripts\activate

(ich hatte ein PowerShell problem als ich venv starten wollte, falls was kommt einfach das eingeben:
Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy RemoteSigned
)

probiert mal das:
python -m pip install -r requirements.txt

wenn das obere nd geht einfach das hier:
python -m pip install --upgrade pip
python -m pip install flask pymongo argon2-cffi
   

APP AUSFÜHREN IM TERMINAL:

python app.py
dann: http://127.0.0.1:5000


Clothing Items Categories: 

TOPS:
1a = oversized/regular tshirts
1b = slimfit tshirts
2 = longsleves
3 = sweatshirt
4 = hoodie
5 = hemd/bluse
6 = tanktops
7 = sonstiges

BOTTOMS:
1 = jeans
2 = stoffhose
3 = jeans skinny
4 = leggings
5 = skirts
6 = shorts
7 = sweatpants
