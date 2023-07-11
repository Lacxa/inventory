import os
import re
import time

import phonenumbers
from PIL import Image
from kivy import utils

import network
from beem import sms as SM
from beem import OTP as tp
from camera4kivy import Preview
from kivy.base import EventLoop
from kivy.clock import Clock, mainthread
from kivy.core.window import Window
from kivy.properties import StringProperty, NumericProperty, ObjectProperty
from kivymd.app import MDApp
from kivymd.toast import toast
from kivymd.uix.textfield import MDTextField
from phonenumbers import carrier
from phonenumbers.phonenumberutil import number_type
from pyzbar.pyzbar import decode
from kivymd.uix.picker import MDDatePicker

from database import Transfer as TR

Window.keyboard_anim_args = {"d": .2, "t": "linear"}
Window.softinput_mode = "below_target"
Clock.max_iteration = 250

if utils.platform != 'android':
    Window.size = [420, 740]


class Scan_Analyze(Preview):
    extracted_data = ObjectProperty(None)

    def analyze_pixels_callback(self, pixels, image_size, image_pos, scale, mirror):

        pimage = Image.frombytes(mode='RGBA', size=image_size, data=pixels)
        list_of_all_barcodes = decode(pimage)

        if list_of_all_barcodes:
            if self.extracted_data:
                self.extracted_data(list_of_all_barcodes[0])
            else:
                print("NOt found")


class NumberField(MDTextField):
    pat = re.compile('[^0-9]')

    def insert_text(self, substring, from_undo=False):

        if len(self.text) == 0 and substring != "0":
            return

        if len(self.text) == 10:
            return

        if len(self.text) == 1 and substring != "6" and substring != "7":
            return

        if not substring.isdigit():
            return

        return super(NumberField, self).insert_text(substring, from_undo=from_undo)


class NumberOnlyField(MDTextField):
    pat = re.compile('[^0-9]')

    def insert_text(self, substring, from_undo=False):

        if len(self.text) == 0 and substring == "0":
            return

        if not substring.isdigit():
            return

        return super(NumberOnlyField, self).insert_text(substring, from_undo=from_undo)


class MainApp(MDApp):
    user_pin = StringProperty('')
    size_x, size_y = Window.size

    # APP
    screens = ['home']
    screens_size = NumericProperty(len(screens) - 1)
    current = StringProperty(screens[len(screens) - 1])

    # Temp
    t_phone = StringProperty("")
    t_name = StringProperty("")

    # QR data
    data_id = StringProperty("")
    get_id = StringProperty("")
    s_id = StringProperty("")

    # Medicine
    name = StringProperty("......................")
    quantity = StringProperty("......................")
    price = StringProperty("......................")
    expire = StringProperty("......................")
    days_to_expire = StringProperty("......................")

    selected_date = StringProperty("Select Transaction Date")
    year = StringProperty("")
    datep = StringProperty("")

    sales = StringProperty("")
    sell = StringProperty("")
    total = StringProperty("---")

    sname = StringProperty("")
    squantity = StringProperty("")
    sprice = StringProperty("")
    sexpire = StringProperty("")

    date = StringProperty("Open date picker")

    # 0682590979
    register = StringProperty("")

    """ CAMERA CONNECTIONS """

    def on_kv_post(self):
        self.root.ids.preview.connect_camera(enable_analyze_pixels=True, default_zoom=0.0)
        print("connected")

    def stop_camera(self):
        self.root.ids.preview.disconnect_camera()

    def on_kv_post2(self):
        self.root.ids.preview2.connect_camera(enable_analyze_pixels=True, default_zoom=0.0)

    def stop_camera2(self):
        self.root.ids.preview2.disconnect_camera()

    def on_kv_post3(self):
        self.root.ids.preview3.connect_camera(enable_analyze_pixels=True, default_zoom=0.0)

    def stop_camera3(self):
        self.root.ids.preview3.disconnect_camera()

    @mainthread
    def got_result(self, result):
        idd = str(result.data)
        type = str(result.type)
        sm = self.root
        if idd:
            idd = idd.replace("b", "")
            idd = idd.replace("'", "")
            if type != "QRCODE":
                self.data_id = idd
                print(self.data_id)
                self.screen_capture("add")
            else:
                toast("show barcode")

    @mainthread
    def get_result(self, result):
        Search_id = str(result.data)
        type = str(result.type)
        sm = self.root
        if Search_id:
            Search_id = Search_id.replace("b", "")
            Search_id = Search_id.replace("'", "")
            if type != "QRCODE":
                self.get_id = Search_id
                print(self.get_id)
                self.screen_capture("search")

            else:
                toast("show barcode")

    @mainthread
    def search_result(self, result):
        sell_id = str(result.data)
        type = str(result.type)
        sm = self.root
        if sell_id:
            sell_id = sell_id.replace("b", "")
            sell_id = sell_id.replace("'", "")
            if type != "QRCODE":
                self.s_id = sell_id
                print(self.s_id)
                self.screen_capture("availability")
                Clock.schedule_once(lambda x: self.sell_medicine(self.s_id), 1)
            else:
                toast("show barcode")

    def build(self):
        pass

    """ REGISTRATION , VERIFICATION AND REMEMBER ME(login) """

    def validate_user(self, phone, name):
        if not self.phone_number_check_admin(phone):
            pass
        elif name == "":
            toast("please enter your password")
        else:
            self.t_phone = phone
            self.t_name = name
            self.phone_verify(phone)
            self.remember_me(phone)

    def phone_verify(self, phone):
        toast('wait a moment')
        tp.req.otp_req(tp.req(), phone)
        self.screen_capture("verify")

    def verify(self, pin):
        if tp.req.verfy(tp.req(), pin):
            Clock.schedule_once(lambda x: self.register_caller(self.t_phone, self.t_name), 1)
        else:
            toast("Try again")

    def phone_number_check_admin(self, phone):
        new_number = ""
        if phone != "" and len(phone) == 10:
            for i in range(phone.__len__()):
                if i == 0:
                    pass
                else:
                    new_number = new_number + phone[i]
            number = "+255" + new_number
            if not carrier._is_mobile(number_type(phonenumbers.parse(number))):
                toast("Please check your phone number!", 1)
                return False
            else:
                self.public_number = number
                return True
        else:
            toast("enter phone number!")

    def register_caller(self, phone, name):
        try:
            TR.pharmacist(TR(), phone, name)
            self.screen_capture("home")
        except:
            toast('OPPs!, No connection')

    def user_login(self, phone, passe):
        if TR.get_login(TR(), phone, passe):
            self.screen_capture("home")
        else:
            toast("Invalid login")

    def remember_me(self, phone):
        with open("register.txt", "w") as fl:
            fl.write(phone)
        fl.close()

    def register_check(self):
        sm = self.root
        file_size = os.path.getsize("register.txt")
        if file_size == 0:
            self.screen_capture("register")
        else:
            sm.current = "register"
            self.screen_capture("login")


    """ MEDICINE FUNCTIONS """

    def add_medicine(self, product_id, name, quantity, price, exp):
        if network.ping_net():
            dates = self.date
            if product_id == "":
                toast("Please scan medicine first")
            elif name == "":
                toast("Please enter name")
            elif quantity == "":
                toast("Please enter quantity")
            elif price == "":
                toast("Please enter price")
            elif dates == "Open date picker":
                toast("please pick expiration date")
            else:
                if TR.register(TR(), product_id, name, quantity, price, exp):
                    toast("Medicine Added successfully")
                else:
                    toast("Medicine already exist")
        else:
            toast("No internet")

    @mainthread
    def delete_product(self, name):
        TR.delete_product(TR(), name)
        self.remove()
        self.display_medicine()
        self.check_medicine(name)

    def remove(self):
        spiner = self.root.ids.spine_del
        spiner.active = True

    def check_medicine(self, id):
        data = TR.fetch_medicine(TR(), id)
        if data == "nodata":
            self.deleted()
        else:
            pass

    def deleted(self):
        spiner = self.root.ids.spine_del
        spiner.active = False

    def scan_medicine(self, ):
        if self.data_id != "":
            button = self.root.ids.med
            button.pos_hint = {'center_x': 1.5, 'center_y': .75}

    def search_medicine(self, product_id):
        if network.ping_net():
            data = TR.fetch_medicine(TR(), product_id)
            if data == "nodata":
                toast("nodata found")

            elif data:
                self.expire = data['expiration_date']
                self.name = data['name']
                self.price = data['price']
                self.quantity = data['quantity']
                self.days_to_expire = data["days_to_exp"]

        else:
            toast("No internet")

    def sell_medicine(self, product_id):
        if network.ping_net():
            data = TR.fetch_medicine(TR(), product_id)
            if data == "nodata":
                self.screen_capture("move")

            elif data:
                self.sexpire = data['expiration_date']
                self.sname = data['name']
                self.sprice = data['price']
                self.squantity = data['quantity']
        else:
            toast("No internet")

    def tes2(self, sell):
        TR.upd(TR(), self.s_id, sell)

    def sell_product(self, sell_quantity):
        self.sell = self.squantity
        self.sales = sell_quantity
        print(sell_quantity, self.sell)

        if int(sell_quantity) > int(self.sell):
            toast("Enter valid quantity")

        elif sell_quantity == "":
            toast("Enter valid quantity")

        elif self.total == "":
            toast("Fill quantity")

        else:
            self.sell = str(int(self.sell) - int(sell_quantity))
            self.tes2(self.sell)
            self.squantity = self.sell
            self.transaction_history()
            self.today_history()
            self.screen_capture("sell")
            toast("sell a success")

    def Total(self, sell_quantity):
        if sell_quantity == "":
            self.total = ""

        elif sell_quantity != "":
            self.total = str(int(sell_quantity) * int(self.sprice))

    def transaction_history(self, ):
        TR.history(TR(), self.s_id, self.sname, self.sales, self.total)

    def today_history(self):
        if network.ping_net():
            self.root.ids.today.data = {}
            history = TR.today_history(TR())

            if not history:
                self.root.ids.today.data.append(
                    {
                        "viewclass": "Notransaction",
                        "name": "No history available!",
                    }
                )
            else:
                for i, y in history.items():
                    self.root.ids.today.data.append(
                        {
                            "viewclass": "Transaction",
                            "name": y["Name"],
                            "sell": y["sell"],
                            "total": y["total"]

                        }
                    )
        else:
            toast("No internet")

    """ DATE FUNCTIONS """

    def on_save(self, instance, value, date_ranges):
        self.date = str(value)

    def on_savu(self, instance, value, date_ranges):
        self.selected_date = str(value)
        two = self.selected_date.strip().split('-')
        self.year = (f"{two[0]}")
        self.datep = (f"{two[1]}_{two[2]}")
        self.display_history()

    def on_cancel(self, instance, value):
        '''Events called when the "CANCEL" dialog box button is clicked.'''


    def show_date_picker(self):
        self.theme_cls.primary_palette = "Blue"
        date_dialog = MDDatePicker()
        date_dialog.bind(on_save=self.on_save, on_cancel=self.on_cancel)
        date_dialog.open()

    def select_date_picker(self):
        self.theme_cls.primary_palette = "Blue"
        date_dialog = MDDatePicker()
        date_dialog.bind(on_save=self.on_savu, on_cancel=self.on_cancel)
        date_dialog.open()

    def on_start(self):
        self.keyboard_hooker()
        Clock.schedule_once(lambda x: self.register_check(), 6)
        # self.request_android_permissions()

    """ KEYBOARD INTEGRATION """

    def keyboard_hooker(self, *args):
        EventLoop.window.bind(on_keyboard=self.hook_keyboard)
        self.find_register()

    def hook_keyboard(self, window, key, *largs):
        print(self.screens_size)
        if key == 27 and self.screens_size > 0:
            print(f"your were in {self.current}")
            last_screens = self.current
            self.screens.remove(last_screens)
            print(self.screens)
            self.screens_size = len(self.screens) - 1
            self.current = self.screens[len(self.screens) - 1]
            self.screen_capture(self.current)
            return True
        elif key == 27 and self.screens_size == 0:
            toast('Press Home button!')
            return True

    """ SCREEN FUNCTIONS """

    def screen_capture(self, screen):
        sm = self.root
        sm.current = screen
        if screen in self.screens:
            pass
        else:
            self.screens.append(screen)
        print(self.screens)
        self.screens_size = len(self.screens) - 1
        self.current = self.screens[len(self.screens) - 1]
        print(f'size {self.screens_size}')
        print(f'current screen {screen}')

    def screen_leave(self):
        print(f"your were in {self.current}")
        last_screens = self.current
        self.screens.remove(last_screens)
        print(self.screens)
        self.screens_size = len(self.screens) - 1
        self.current = self.screens[len(self.screens) - 1]
        self.screen_capture(self.current)

    """ DISPENSING FUNCTIONS """

    def display_history(self):
        if network.ping_net():
            self.root.ids.attendi.data = {}
            history = TR.fetch_history(TR(), self.year, self.datep)

            if not history:
                self.root.ids.attendi.data.append(
                    {
                        "viewclass": "Notransaction",
                        "name": "No history available!",
                    }
                )
            else:
                for i, y in history.items():
                    self.root.ids.attendi.data.append(
                        {
                            "viewclass": "Transaction",
                            "name": y["Name"],
                            "sell": y["sell"],
                            "total": y["total"]

                        }
                    )
        else:
            toast("No internet")

    def display_medicine(self):
        if network.ping_net():
            self.root.ids.attend.data = {}
            product = TR.get_medicine(TR())
            if not product:
                self.root.ids.attend.data.append(
                    {
                        "viewclass": "Medicine",
                        "name": "No medicine yet!",
                    }
                )
            else:
                for i, y in product.items():
                    self.root.ids.attend.data.append(
                        {
                            "viewclass": "Medicine",
                            "name": y["name"],
                            "price": y["price"],
                            "quantity": y["quantity"],
                            "expire": y["expiration_date"],
                            "idd": i
                        }
                    )

        else:
            toast("No internet")

    """ SENDING MESSAGE """

    def find_register(self):
        self.register = TR.get_register(TR())
        self.expired()

    def expired(self):
        data = TR.expire(TR())

        for i, y in data.items():
            date = y["days_to_exp"]
            name = y["name"],

            if date <= 30:
                self.send_message(date, name)

    def send_message(self, date, name):
        SM.send_sms(self.register, date, name)

    """ REQUEST ANDROID PERMISSIONS """

    def request_android_permissions(self):
        from android.permissions import request_permissions, Permission

        def callback(permissions, results):
            if all([res for res in results]):
                print("callback. All permissions granted.")
            else:
                print("callback. Some permissions refused.")

        request_permissions([Permission.CAMERA], callback)


MainApp().run()
