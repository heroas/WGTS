import kivy
kivy.require('1.10.0')
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.utils import get_color_from_hex
from kivymd.color_definitions import colors
import Global
from kivymd.accordion import MDAccordion, MDAccordionItem, MDAccordionSubItem
from kivymd.list import OneLineListItem, TwoLineListItem
from tinydb import TinyDB, Query
from NyaaPy import Nyaa
import home
import requests
import os
import sys
import subprocess
from services import anilist_api
import functools

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

class Home(Screen):
    def load(self):
        anilist_api.get_airing_schedule(100166)


    def remove_accord_test(self):
        print(self.ids.accord_box)
        self.ids.accord_box.remove_widget(self.ids.ani_list)

    def add_accord_test(self):
        accord = MDAccordion()
        accord.orientation = 'vertical'
        accord.id = 'ani_list'
        accord.md_bg_color = Global.SEASON_COLOR
        accord.specific_text_color = get_color_from_hex('#000000')

        self.ids.accord_box.add_widget(accord)


    def testin_nyaapy(self):
        animeList = Nyaa.search(keyword="Shoukoku no Altair", category=1, subcategory=2)
        Global.Test = animeList[0]["magnet"]
    pass
