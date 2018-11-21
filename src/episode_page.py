import kivy
kivy.require('1.10.0')
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.utils import get_color_from_hex
from kivymd.color_definitions import colors
from kivy.uix.image import Image, AsyncImage
import Global
from kivymd.accordion import MDAccordion, MDAccordionItem, MDAccordionSubItem
from kivymd.list import OneLineListItem, TwoLineListItem, MDList
from kivymd.bottomsheet import MDListBottomSheet, MDGridBottomSheet
from kivy.uix.scrollview import ScrollView
from kivymd.snackbar import Snackbar
from tinydb import TinyDB, Query
from NyaaPy import Nyaa
import home
import requests
import os
import sys
import time
import subprocess
from services import anilist_api
import functools
import shutil



from async_gui.engine import Task
from async_gui.toolkits.kivy import KivyEngine

engine = KivyEngine()
romaji_list = []
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

def download_file(url, name):
    r = requests.get(url, allow_redirects=True)
    print(os.path.splitext(name)[0])
    torrent_name = os.path.splitext(name)[0]
    open('torrents/'+torrent_name+'.torrent', 'wb').write(r.content)
    Snackbar('Torrent '+ torrent_name + ' sucessfully downloaded to torrents folder.').show()

def freshen_up_search(name, episode):
    episode_string = str(episode)
    if episode < 10:
        episode_string = '0' + episode_string

    return name.replace('-',' ') + ' - ' + episode_string

class Episode_Page(Screen):

    def reset_list(self):
        fresh_list = self.get_fresh_list()
        self.add_to_list(Global.ROMAJI_LIST,fresh_list)
        self.add_to_list(Global.ENG_LIST,fresh_list)
        self.add_to_list(Global.CUSTOM_LIST,fresh_list)

    def add_to_list(self, anime_list, list_widget):
        for torrent in anime_list:
            torrent_details = 'seeders: '+ torrent["seeders"]+' | leechers: ' + torrent["leechers"] + ' | size: '+ torrent["size"] + ' | downloads: '+ torrent["completed_downloads"]
            anime_list_item = TwoLineListItem(text=torrent["name"],secondary_text=torrent_details)
            anime_list_item.on_release = functools.partial(self.open_bottom_sheet, torrent)
            list_widget.add_widget(anime_list_item)

    def get_fresh_list(self):
        for child in self.ids.list_container.children:
            self.ids.list_container.remove_widget(child)

        sv = ScrollView()
        new_list = MDList()
        sv.add_widget(new_list)

        self.ids.list_container.add_widget(sv)
        return new_list


    def root():
        return self.root

    def open_bottom_sheet(self, torrent):
        print(torrent)
        bs = MDListBottomSheet()
        bs.add_item(torrent["name"], lambda x: print('heyo'))
        bs.add_item("Download by magnet", lambda x: open_magnet(torrent["magnet"]),
                    icon='download')
        bs.add_item("Download torrent file", lambda x: download_file(torrent["download_url"],torrent["name"]), icon='file')
        bs.open()

    def search_with_episode(self, anime, episode, filename):
        self.ids.anime_img.source = 'thumbnails/' + anime["romaji_name"] + '.jpg'

        Global.CUSTOM_LIST = []
        fresh_list = self.get_fresh_list()
        self.ids.search_param.text = anime["romaji_name"] + ' episode ' + str(episode)

        romaji_search = freshen_up_search(anime["romaji_name"], episode)
        eng_search = freshen_up_search(anime["eng_name"], episode)

        print(romaji_search)
        print(eng_search)
        if anime["romaji_name"] != str(None):
            anime_list_romaji = Nyaa.search(keyword=romaji_search, category=1, subcategory=2)
            Global.ROMAJI_LIST = anime_list_romaji
            self.add_to_list(anime_list_romaji,fresh_list)

        if anime["eng_name"] != str(None):
            anime_list_eng = Nyaa.search(keyword=eng_search, category=1, subcategory=2)
            Global.ENG_LIST = anime_list_eng
            self.add_to_list(anime_list_eng,fresh_list)


    def search(self, string):
        self.ids.anime_img.source = 'thumbnails/default-thumbnail.jpg'

        Global.ROMAJI_LIST = []
        Global.ENG_LIST = []
        fresh_list = self.get_fresh_list()
        self.ids.search_param.text = string
        anime_list = Nyaa.search(keyword=string , category=1, subcategory=2)
        Global.CUSTOM_LIST = anime_list
        self.add_to_list(anime_list,fresh_list)

    def go_back(self):
        self.manager.transition.direction = 'right'
        self.manager.current = 'home'
    pass
