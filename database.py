from datetime import datetime


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

    def register(self, product_id, name, quantity, price, exp):
        if True:
            import firebase_admin
            firebase_admin._apps.clear()
            from firebase_admin import credentials, initialize_app, db
            if not firebase_admin._apps:
                cred = credentials.Certificate("credentials/medics-inventorry-firebase-adminsdk-jgzwk-9a41481b87.json")
                initialize_app(cred, {'databaseURL': 'https://medics-inventorry-default-rtdb.firebaseio.com/'})
                ref = db.reference('Inventory').child('Shop').child("Products").child(product_id)
                print("uploaded")
                ref.set(
                    {
                        "name": name,
                        "quantity": quantity,
                        "price": price,
                        "expiration_date": exp,
                    }
                )
    def upd(self, product_id, sell):
        if True:
            import firebase_admin
            firebase_admin._apps.clear()
            from firebase_admin import credentials, initialize_app, db
            if not firebase_admin._apps:
                cred = credentials.Certificate("credentials/medics-inventorry-firebase-adminsdk-jgzwk-9a41481b87.json")
                initialize_app(cred, {'databaseURL': 'https://medics-inventorry-default-rtdb.firebaseio.com/'})
                ref = db.reference('Inventory').child('Shop').child("Products").child(product_id)
                print("uploaded")
                ref.update(
                    {
                        "quantity": sell,
                    }
                )


    def fetch_medicine(self, product_id):
        if True:
            import firebase_admin
            firebase_admin._apps.clear()
            from firebase_admin import credentials, initialize_app, db
            try:
                if not firebase_admin._apps:
                    cred = credentials.Certificate(
                        "credentials/medics-inventorry-firebase-adminsdk-jgzwk-9a41481b87.json")
                    initialize_app(cred, {'databaseURL': 'https://medics-inventorry-default-rtdb.firebaseio.com/'})
                    ref = db.reference('Inventory').child('Shop').child("Products").child(product_id)
                    data = ref.get()
                    print(data)
                    return data
            except:
                return False

    def hello(self):
        pass
