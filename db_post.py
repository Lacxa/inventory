import firebase_admin

firebase_admin._apps.clear()
from firebase_admin import credentials, initialize_app, db

if not firebase_admin._apps:
    cred = credentials.Certificate("/home/noface/PycharmProjects/inventory/medics-inventorry-firebase-adminsdk-jgzwk-9a41481b87.json")
    initialize_app(cred, {'databaseURL': 'https://medics-inventorry-default-rtdb.firebaseio.com/'})
    ref = db.reference('Register').child("phone").child("passward")
    print("New Start")
    ref.set(
        {
            "user_phone": "0714069014",
            "pasword": "kkk",

        }
    )
    print("Done")




