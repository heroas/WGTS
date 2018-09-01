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
from kivy.utils import get_color_from_hex
from kivymd.color_definitions import colors
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
import home
import requests
import os
import sys
import subprocess
from NyaaPy import Nyaa
import datetime
from tinydb import TinyDB, Query



def set_season():

    date = datetime.datetime.now()
    month = date.strftime("%m")
    year = date.strftime("%Y")

    if month in ('01','02','03'):
        Global.SEASON_NAME = "Winter"
    elif month in ('04','05','06'):
        Global.SEASON_NAME = "Spring"
    elif month in ('07','08','09'):
        Global.SEASON_NAME = "Summer"
    else:
        Global.SEASON_NAME = "Fall"

    season_color_switcher = {
        "Winter": get_color_from_hex(colors['LightBlue']['300']),
        "Spring": get_color_from_hex(colors['Green']['300']),
        "Summer": get_color_from_hex(colors['Yellow']['200']),
        "Fall": get_color_from_hex(colors['Orange']['500'])
        }
    season_color_dark_switcher = {
        "Winter": get_color_from_hex(colors['LightBlue']['600']),
        "Spring": get_color_from_hex(colors['Green']['600']),
        "Summer": get_color_from_hex(colors['Red']['600']),
        "Fall": get_color_from_hex(colors['Orange']['600'])
        }

    Global.SEASON_COLOR = season_color_switcher.get(Global.SEASON_NAME)
    Global.SEASON_COLOR_DARK = season_color_dark_switcher.get(Global.SEASON_NAME)
    Global.SEASON_YEAR = year

    print(Global.SEASON_NAME)
    print(Global.SEASON_COLOR)

def load_create_tinydb():
    seasonYear = Global.SEASON_NAME + Global.SEASON_YEAR
    Global.DB_FILE = seasonYear + '.json'
    db = TinyDB(Global.DB_FILE)
    #db.insert({'anime': 'Saumrai Champloo', 'season': seasonYear, 'episodes_retrieved': 24, 'magnet_link': 'asdhjfasudtvhb' })


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

def resource_path(relative):
    if hasattr(sys, "_MEIPASS"):
        return os.path.join(sys._MEIPASS, relative)
    return os.path.join(relative)


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
        main_widget.ids.scr_mngr.add_widget(home.Home(name='home'))

        return main_widget


if __name__ == '__main__':
    set_season()
    load_create_tinydb()
    WGTS().run()
