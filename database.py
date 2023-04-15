from datetime import datetime

import firebase_admin

firebase_admin._apps.clear()
from firebase_admin import credentials, initialize_app, db

if not firebase_admin._apps:
    cred = credentials.Certificate("credentials/medics-inventorry-firebase-adminsdk-jgzwk-9a41481b87.json")
    initialize_app(cred, {'databaseURL': 'https://medics-inventorry-default-rtdb.firebaseio.com/'})
    ref = db.reference('Register').child("phone")
    print("New Start")
    ref.set(
        {
            "user_phone": "0714069084",
            "pasword": "kkk",

        }
    )
    print("Done")


class Transfer:
    current_time = str(datetime.now())
    date, time = current_time.strip().split()
    week_day = ""
    day = ""
    point = '1'
    bought = '1'
    loyal = '1'
    orders = '1'
    number = 0
    order_id = '123'

    def register(self, phone, name):
        if True:
            import firebase_admin
            firebase_admin._apps.clear()
            from firebase_admin import credentials, initialize_app, db
            if not firebase_admin._apps:
                cred = credentials.Certificate("credentials/medics-inventorry-firebase-adminsdk-jgzwk-9a41481b87.json")
                initialize_app(cred, {'databaseURL': 'https://medics-inventorry-default-rtdb.firebaseio.com/'})
                print("Starting deployment....", int(phone))

                ref = db.reference('Inventory').child('Users')
                users = ref.get()
                if phone in users:
                    print('It there')
                else:
                    ref = db.reference('Inventory').child("Users").child(phone)
                    print("horray!!!")
                    ref.set(
                        {
                            'user_name': name,
                            'phone': phone,

                        })


#Transfer.register(Transfer(), "0714069014", "123")
