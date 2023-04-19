import re

import phonenumbers
from PIL import Image
from camera4kivy import Preview
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
    screens = ['entrance']
    screens_size = NumericProperty(len(screens) - 1)
    current = StringProperty(screens[len(screens) - 1])

    # Temp
    t_phone = StringProperty("")
    t_name = StringProperty("")

    # QR data
    data_id = StringProperty("")

    # Medicine
    name = StringProperty("......................")
    quantity = StringProperty("......................")
    price = StringProperty("......................")
    expire = StringProperty("......................")
    sell = StringProperty("")

    sname = StringProperty("")
    squantity = StringProperty("")
    sprice = StringProperty("")
    sexpire = StringProperty("")

    date = StringProperty("Open date picker")

    @mainthread
    def on_kv_post(self):
        self.root.ids.preview.connect_camera(enable_analyze_pixels=True, default_zoom=0.0)

    def stop_camera(self):
        self.root.ids.preview.disconnect_camera()

    @mainthread
    def on_kv_post2(self):
        self.root.ids.preview2.connect_camera(enable_analyze_pixels=True, default_zoom=0.0)

    def stop_camera2(self):
        self.root.ids.preview2.disconnect_camera()

    @mainthread
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
        self.root.ids.ti.text = str(result)

    """if sm.current == "camera":
            self.screen_capture("add")
        else:
            self.screen_capture("search")"""

    @mainthread
    def get_result(self, result):
        idd = str(result.data)
        type = str(result.type)
        sm = self.root
        if idd:
            idd = idd.replace("b", "")
            idd = idd.replace("'", "")
            if type != "QRCODE":
                self.data_id = idd
                print(self.data_id)
                self.screen_capture("search")
            else:
                toast("show barcode")
        self.root.ids.ti.text = str(result)

    @mainthread
    def search_result(self, result):
        idd = str(result.data)
        type = str(result.type)
        sm = self.root
        if idd:
            idd = idd.replace("b", "")
            idd = idd.replace("'", "")
            if type != "QRCODE":
                self.data_id = idd
                print(self.data_id)
                self.search_medicines(self.data_id)
            else:
                toast("show barcode")
        self.root.ids.ti.text = str(result)

    def build(self):

        pass

    def remember_me(self, phone, dust, name):
        with open("credential/admin.txt", "w") as fl:
            fl.write(phone + "\n")
            fl.write(dust)
        with open("credential/admin_info.txt", "w") as ui:
            ui.write(name)
        fl.close()
        ui.close()

    def validate_user(self, phone, name):
        if not self.phone_number_check_admin(phone):
            toast("please enter your phone number correctly")
        elif name == "":
            toast("please enter your password")
        else:
            self.t_phone = phone
            self.t_name = name
            self.phone_verify(phone)

    def phone_verify(self, phone):
        from beem import OTP as tp
        toast('wait a moment')
        tp.req.otp_req(tp.req(), phone)
        self.screen_capture("verify")

    def verify(self, pin):
        from beem import OTP as tp
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
            TR.register(TR(), phone, name)
            self.screen_capture("home")
        except:
            toast('OPPs!, No connection')

    def add_medicine(self, product_id, name, quantity, price, exp):
        dates = self.date
        if product_id is "":
            toast("Please scan medicine first")
        elif name == "":
            toast("Please enter name")
        elif quantity == "":
            toast("Please enter quantity")
        elif price == "":
            toast("Please enter price")
        elif exp == dates == "Open date picker":
            toast("please pick expiration date")
        else:

            from database import Transfer as TR
            try:
                TR.register(TR(), product_id, name, quantity, price, exp)
                toast("Medicine Added successfully")
            except:
                toast("No network")

    def search_medicine(self, product_id):
        if TR.fetch_medicine(TR(), product_id):
            data = TR.fetch_medicine(TR(), product_id)
            self.sexpire = data['expiration_date']
            self.sname = data['name']
            self.sprice = data['price']
            self.squantity = data['quantity']
            self.screen_capture("result")

        else:
            toast("No Product Found")

    def search_medicines(self, product_id):
        if TR.fetch_medicine(TR(), product_id):
            data = TR.fetch_medicine(TR(), product_id)
            self.sexpire = data['expiration_date']
            self.sname = data['name']
            self.sprice = data['price']
            self.squantity = data['quantity']
            self.screen_capture("availability")

        else:
            self.screen_capture("move")

    def tes2(self, sell):

        TR.upd(TR(), self.data_id, sell)

    def sell_product(self, sell_quantity):
        self.sell = self.squantity

        print(sell_quantity, self.sell)

        if int(sell_quantity) > int(self.sell):
            toast("Enter valid quantity")

        else:
            self.sell = str(int(self.sell) - int(sell_quantity))
            self.tes2(self.sell)
            self.squantity = self.sell
            toast("sell a success")

    def on_save(self, instance, value, date_ranges):
        self.date = str(value)

    def on_cancel(self, instance, value):
        '''Events called when the "CANCEL" dialog box button is clicked.'''

    def show_date_picker(self):
        self.theme_cls.primary_palette = "Blue"
        date_dialog = MDDatePicker()
        date_dialog.bind(on_save=self.on_save, on_cancel=self.on_cancel)
        date_dialog.open()

    def scan_medicine(self, ):
        if self.data_id != "":
            button = self.root.ids.med
            button.pos_hint = {'center_x': 1.5, 'center_y': .75}

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


MainApp().run()
