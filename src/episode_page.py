import kivy
kivy.require('1.10.0')
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.utils import get_color_from_hex
from kivymd.color_definitions import colors
import Global
from kivymd.accordion import MDAccordion, MDAccordionItem, MDAccordionSubItem
from kivymd.list import OneLineListItem, TwoLineListItem
from kivymd.bottomsheet import MDListBottomSheet, MDGridBottomSheet
from tinydb import TinyDB, Query
from NyaaPy import Nyaa
import home
import requests
import os
import sys
import subprocess
from services import anilist_api
import functools



from async_gui.engine import Task
from async_gui.toolkits.kivy import KivyEngine

engine = KivyEngine()
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

class Episode_Page(Screen):

    def add_to_list(self, anime_list):
        for torrent in anime_list:
            print(torrent["name"])
            olli = OneLineListItem(text=torrent["name"])
            olli.on_release = functools.partial(self.open_bottom_sheet, torrent)
            self.ids.ml_ep.add_widget(olli)

    def root():
        return self.root

    def open_bottom_sheet(self, torrent):
        print(torrent)
        bs = MDListBottomSheet()
        bs.add_item(torrent["name"], lambda x: print('heyo'))
        bs.add_item("Here's an item with an icon", lambda x: open_magnet(torrent["magnet"]),
                    icon='clipboard-account')
        bs.add_item("Here's another!", lambda x: x, icon='nfc')
        bs.open()

    def search(self, anime, episode):
        self.ids.search_param.text = anime["romaji_name"] + ' episode ' + str(episode)
        anime_list_romaji = Nyaa.search(keyword=anime["romaji_name"] +" " + str(episode) , category=1, subcategory=2)
        anime_list_eng = Nyaa.search(keyword=anime["eng_name"] +" " + str(episode) , category=1, subcategory=2)
        self.add_to_list(anime_list_romaji)
        self.add_to_list(anime_list_eng)
        Global.MAIN_WIDGET.ids.toolbar.left_action_items = [['arrow-left', lambda x: self.go_back()]]

    def go_back(self):
        self.manager.transition.direction = 'right'
        self.manager.current = 'home'
        Global.MAIN_WIDGET.ids.toolbar.left_action_items = [['menu', lambda x: self.root.toggle_nav_drawer()]]
    pass
