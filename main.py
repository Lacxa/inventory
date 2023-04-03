import re

from kivy.core.window import Window
from kivymd.app import MDApp
from kivymd.uix.textfield import MDTextField

Window.size = [360,640]

class MainApp(MDApp):
    def build(self):

        pass



class NumberOnlyField(MDTextField):
    pat = re.compile('[^0-9]')

    def insert_text(self, substring, from_undo=False):

        pat = self.pat

        if "." in self.text:
            s = re.sub(pat, "", substring)

        else:
            s = ".".join([re.sub(pat, "", s) for s in substring.split(".", 1)])

        return super(NumberOnlyField, self).insert_text(s, from_undo=from_undo)


"""def remember_me(self, phone, dust, name):
    with open("credential/admin.txt", "w") as fl:
        fl.write(phone + "\n")
        fl.write(dust)
    with open("credential/admin_info.txt", "w") as ui:
        ui.write(name)
    fl.close()
    ui.close()"""

MainApp().run()
