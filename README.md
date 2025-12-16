This is the repository for our Software Engineering Project "MisMatch"

Clothes are filtered by numbers:
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


TUTORIAL:
https://www.mongodb.com/try/download/community -> MongoDB runterladen

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
python -m pip install > requirements.txt       

wenn das obere nd geht einfach das hier:
python -m pip install --upgrade pip
python -m pip install flask pymongo argon2-cffi
   

APP AUSFÜHREN IM TERMINAL:

python app.py
dann: http://127.0.0.1:5000



Beim Download von MongoDB unbedingt MongoDB Compass auch herunterladen.

neue Connection starten:

URI: mongodb://localhost:27017

NAME: MisMatch

COLOR: optional, wie ihr wollt

dann Save & Connect

dann sollte sie schonmal existieren und dann kann man schon herumclicken.
bei users, sollten die erstellen User drinnen sein, mit Username und gehashtem Passwort (und auch createdAt)

dann noch bitte:
auf users gehen, 
dann steht dort INDEXES das anclicken und einen neuen Index erstellen,
das ist damit man nicht doppelte Usernames hat:

Create index -> field: username -> Order: Ascending -> unique