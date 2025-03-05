import pyrebase

firebaseConfig = {
    "apiKey": "AIzaSyDSFM4hU69Sm9ny4BWmNPBoqXWxexXPQv0",
    "authDomain": "carregar-regarcas-ende.firebaseapp.com",
    "projectId": "carregar-regarcas-ende",
     "databaseURL": "https://carregar-regarcas-ende-default-rtdb.firebaseio.com/",
    "storageBucket": "carregar-regarcas-ende.firebasestorage.app",
    "messagingSenderId": "517171228824",
    "appId": "1:517171228824:web:2b64a6028d2b1ba4c320ed",
    "measurementId": "G-0ZVKCESSW7"
}

firebase = pyrebase.initialize_app(firebaseConfig)
db = firebase.database()