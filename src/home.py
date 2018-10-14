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
from kivymd.snackbar import Snackbar

from async_gui.engine import Task
from async_gui.toolkits.kivy import KivyEngine

engine = KivyEngine()

class Home(Screen):

    def get_curr(self):
        services.get_next_airing_episode()
    def navigate(self, route):
        if route is 'home':
            Global.HOME_CLASS.load_anime_list()
            self.root.ids.scr_mngr.transition.direction = 'left'
        else:
            self.root.ids.scr_mngr.transition.direction = 'right'

        self.root.ids.scr_mngr.current = route

    @engine.async
    def open_episode_page_with_model(self, episode, anime, *_):
        print('aight lets go')
        Global.MAIN_WIDGET.ids.home.ids.home_spinner.active = True
        Snackbar(
            text="Fetching torrents for: "+ anime["romaji_name"]+ " Ep " + str(episode), duration=2).show()
        self.ids.home_spinner.active = True
        yield Task(functools.partial(Global.EPISODE_PAGE_CLASS.search_with_episode,anime,episode))
        self.manager.transition.direction = 'left'
        self.manager.current = 'ep_page'
        Global.MAIN_WIDGET.ids.home.ids.home_spinner.active = False

    @engine.async
    def open_episode_page_with_string(self, string, *_):
        print('aight lets go')
        Global.MAIN_WIDGET.ids.home.ids.home_spinner.active = True
        Snackbar(
            text="Fetching torrents for: "+ string, duration=2).show()
        self.ids.home_spinner.active = True
        yield Task(functools.partial(Global.EPISODE_PAGE_CLASS.search,string))
        self.manager.transition.direction = 'left'
        self.manager.current = 'ep_page'
        Global.MAIN_WIDGET.ids.home.ids.home_spinner.active = False

    def load_anime_list(self):

        db = TinyDB(Global.DB_FILE)
        anime_db = db.all()

        home_anime_list = Global.MAIN_WIDGET.ids.home.ids.home_anime_list
        for anime in anime_db:
            print('processing ' + anime["romaji_name"])
            start_fetching_episodes_from =  0
            if anime["romaji_name"] not in Global.ANIME_LIST:
                print('Gonna start then')
                anime_item = MDAccordionItem();
                anime_item.icon = 'movie'
                anime_item.title = anime["romaji_name"]
                home_anime_list.add_widget(anime_item)
                if anime["episodes_out"] > 50:
                    start_fetching_episodes_from = anime["episodes_out"] - 50

                for episode in range(start_fetching_episodes_from, anime["episodes_out"]):
                    anime_sub_item = MDAccordionSubItem(parent_item = anime_item, text = 'Episode ' + str(episode + 1))
                    anime_sub_item.on_release = functools.partial(self.open_episode_page_with_model, episode + 1, anime)
                    anime_item.add_widget(anime_sub_item)
                Global.ANIME_LIST.append(anime["romaji_name"])

        print(home_anime_list)

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
