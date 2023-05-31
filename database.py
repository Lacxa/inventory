from datetime import datetime

from kivymd.toast import toast

import network


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
        if network.ping_net():
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
            return True

        else:
            toast("No internet")

    def upd(self, product_id, sell):
        if network.ping_net():
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

        else:
            toast("No internet")

    def fetch_medicine(self, product_id):
            import firebase_admin
            firebase_admin._apps.clear()
            from firebase_admin import credentials, initialize_app, db
            if not firebase_admin._apps:
                cred = credentials.Certificate(
                    "credentials/medics-inventorry-firebase-adminsdk-jgzwk-9a41481b87.json")
                initialize_app(cred, {'databaseURL': 'https://medics-inventorry-default-rtdb.firebaseio.com/'})
                ref = db.reference('Inventory').child('Shop').child("Products")
                data = ref.get()

                if product_id in data:

                    return data[product_id]
                else:

                    return "nodata"

    def get_sell(self, p_i):
            import firebase_admin
            firebase_admin._apps.clear()
            from firebase_admin import credentials, initialize_app, db
            if not firebase_admin._apps:
                cred = credentials.Certificate("credentials/medics-inventorry-firebase-adminsdk-jgzwk-9a41481b87.json")
                initialize_app(cred, {'databaseURL': 'https://medics-inventorry-default-rtdb.firebaseio.com/'})
                try:
                    ref = db.reference('Inventory').child('Shop').child("History").child(self.year()).child(self.month_date())
                    data = ref.get()

                    if p_i in data:
                        sell = data[p_i]["sell"]
                        total = data[p_i]["total"]

                        return [sell, total]
                    else:

                        return False
                except:

                    return False


    def history(self, p_i, name, sell, total):
            import firebase_admin
            firebase_admin._apps.clear()
            from firebase_admin import credentials, initialize_app, db
            if not firebase_admin._apps:
                cred = credentials.Certificate("credentials/medics-inventorry-firebase-adminsdk-jgzwk-9a41481b87.json")
                initialize_app(cred, {'databaseURL': 'https://medics-inventorry-default-rtdb.firebaseio.com/'})
                sells = self.get_sell(p_i)
                if sells:
                    sell_new = str(int(sells[0]) + int(sell))
                    total_new = str(int(sells[1]) + int(total))

                    ref = db.reference('Inventory').child('Shop').child("History").child(self.year()).child(self.month_date()).child(p_i)

                    ref.update(
                        {
                            "Name": name,
                            "sell": sell_new,
                            "total": total_new

                        }
                    )
                else:
                    ref = db.reference('Inventory').child('Shop').child("History").child(self.year()).child(
                        self.month_date()).child(p_i)

                    ref.set(
                        {
                            "Name": name,
                            "sell": sell,
                            "total": total

                        }
                    )


    def fetch_history(self, year, datep):
        import firebase_admin
        firebase_admin._apps.clear()
        from firebase_admin import credentials, initialize_app, db
        if not firebase_admin._apps:
            cred = credentials.Certificate("credentials/medics-inventorry-firebase-adminsdk-jgzwk-9a41481b87.json")
            initialize_app(cred, {'databaseURL': 'https://medics-inventorry-default-rtdb.firebaseio.com/'})
            ref = db.reference('Inventory').child('Shop').child("History").child(year).child(datep)
            data = ref.get()

            return data
    def get_medicine(self):
        import firebase_admin
        firebase_admin._apps.clear()
        from firebase_admin import credentials, initialize_app, db
        if not firebase_admin._apps:
            cred = credentials.Certificate(
                "credentials/medics-inventorry-firebase-adminsdk-jgzwk-9a41481b87.json")
            initialize_app(cred, {'databaseURL': 'https://medics-inventorry-default-rtdb.firebaseio.com/'})
            ref = db.reference('Inventory').child('Shop').child("Products")
            data = ref.get()

            return data


    def year(self):
        current_time = str(datetime.now())
        date, time = current_time.strip().split()
        y, m, d = date.strip().split("-")

        return y

    def month_date(self):
        current_time = str(datetime.now())
        date, time = current_time.strip().split()
        y, m, d = date.strip().split("-")

        return f"{m}_{d}"


#Transfer.fetch_history(Transfer(), "2023", "05_11")