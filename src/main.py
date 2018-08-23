# -*- coding: utf-8 -*-
import kivy
kivy.require('1.10.0')


from kivy.app import App
from kivy.lang import Builder
from kivy.metrics import dp
from kivy.properties import ObjectProperty
from kivy.uix.image import Image
from kivy.config import Config
from kivy.uix.screenmanager import ScreenManager, Screen
Config.set('graphics', 'width', '1080')
Config.set('graphics', 'height', '720')
from kivymd.bottomsheet import MDListBottomSheet, MDGridBottomSheet
from kivymd.button import MDIconButton
from kivymd.date_picker import MDDatePicker
from kivymd.dialog import MDDialog
from kivymd.label import MDLabel
from kivymd.list import ILeftBody, ILeftBodyTouch, IRightBodyTouch, BaseListItem
from kivymd.list import OneLineListItem, TwoLineListItem
from kivymd.material_resources import DEVICE_TYPE
from kivymd.navigationdrawer import MDNavigationDrawer, NavigationDrawerHeaderBase
from kivymd.selectioncontrols import MDCheckbox
from kivymd.menu import MDDropdownMenu
from kivymd.snackbar import Snackbar
from kivymd.theming import ThemeManager
from kivymd.time_picker import MDTimePicker
import Global
import criterea_selection
import requests
import os
import sys
import subprocess
import sqlite3

conn = sqlite3.connect('test.db')

print ("Opened database successfully");
try:
    conn.execute('''SELECT * FROM {} WHERE type='table' ''')
    print ("Table created successfully");
except:
    print ("Table Already There")


def open_magnet(magnet):
        """Open magnet according to os."""
        if sys.platform.startswith('linux'):
            subprocess.Popen(['xdg-open', magnet])
        elif sys.platform.startswith('win32'):
            os.startfile(magnet)
        elif sys.platform.startswith('cygwin'):
            os.startfile(magnet)
        elif sys.platform.startswith('darwin'):
            subprocess.Popen(['open', magnet],
                             stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        else:
            subprocess.Popen(['xdg-open', magnet],
                             stdout=subprocess.PIPE, stderr=subprocess.PIPE)
class Criterea():
    Genres = []
    Names = []
    Quality = '720'

critereas = Criterea()

def resource_path(relative):
    if hasattr(sys, "_MEIPASS"):
        return os.path.join(sys._MEIPASS, relative)
    return os.path.join(relative)


class Home(Screen):
    pass

class WGTS(App):
    theme_cls = ThemeManager()
    previous_date = ObjectProperty()
    title = "What's Good This Season?"
    quality_items = [{'viewclass': 'MDMenuItem','text': 'Example item'}]
    quality_dropDown = MDDropdownMenu(items=[{'viewclass': 'MDMenuItem','text': 'Example item'}], width_mult = 4)

    def on_touch(touch):
        Snackbar(text=str(touch.pos)).show()

    quality_dropDown.on_touch_down = on_touch

    def root():
        return self.root

    def build(self):
        kv_file = resource_path(os.path.join('templates', 'nav.kv'))
        main_widget = Builder.load_file(kv_file)
        main_widget.ids.scr_mngr.add_widget(criterea_selection.Criterea_Selection(name='crits'))
        return main_widget

if __name__ == '__main__':
    WGTS().run()
