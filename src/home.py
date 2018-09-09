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

def load():
    db = TinyDB(Global.DB_FILE)
    anime_db = db.all()

    for anime in anime_db:
        anime_item = MDAccordionItem();
        anime_item.icon = 'movie'
        anime_item.title = anime["anime"]
        Global.MAIN_WIDGET.ids.home.ids.ani_list.add_widget(anime_item)
        for episode in range(0, anime["episodes_retrieved"]):
            anime_sub_item = MDAccordionSubItem(parent_item = anime_item, text = 'Episode ' + str(episode + 1))
            anime_sub_item.on_release = functools.partial(open_magnet, Global.Test)
            anime_item.add_widget(anime_sub_item)

class Home(Screen):
    load()

    def testin_nyaapy(self):
        animeList = Nyaa.search(keyword="Shoukoku no Altair", category=1, subcategory=2)
        Global.Test = animeList[0]["magnet"]
    pass
