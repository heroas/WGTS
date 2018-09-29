# -*- coding: utf-8 -*-
import kivy
kivy.require('1.10.0')


from kivy.app import App
from kivy.lang import Builder
from kivy.metrics import dp
from kivy.properties import ObjectProperty
from kivy.uix.image import Image
from kivy.config import Config
from kivy.uix.scrollview import ScrollView
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
from kivymd.list import OneLineListItem, TwoLineListItem, MDList
from kivymd.material_resources import DEVICE_TYPE
from kivymd.navigationdrawer import MDNavigationDrawer, NavigationDrawerHeaderBase
from kivymd.selectioncontrols import MDCheckbox
from kivymd.menu import MDDropdownMenu
from kivymd.snackbar import Snackbar
from kivymd.theming import ThemeManager
from kivymd.time_picker import MDTimePicker
from kivymd.accordion import MDAccordion, MDAccordionItem, MDAccordionSubItem
import functools
import Global
import criterea_selection
import home
import episode_page
import requests
import os
import sys
import subprocess
from NyaaPy import Nyaa
import datetime
from tinydb import TinyDB, Query


import kivy.core.window as window
from kivy.cache import Cache
from kivy.base import EventLoop

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

def load_create_tinydb():
    seasonYear = Global.SEASON_NAME + Global.SEASON_YEAR
    Global.DB_FILE = seasonYear + '.json'
    db = TinyDB(Global.DB_FILE)


def resource_path(relative):
    if hasattr(sys, "_MEIPASS"):
        return os.path.join(sys._MEIPASS, relative)
    return os.path.join(relative)

def open_magnet(stri):
    print(stri)

class WGTS(App):
    theme_cls = ThemeManager()
    previous_date = ObjectProperty()
    title = "What's Good This Season?"

    def root():
        return self.root

    def open_episode_page(self, episode, anime_name, main_widget):
        print(episode)
        print(anime_name)
        Global.EPISODE_PAGE_CLASS.sayhey()
        # episode_page_list = main_widget.ids.ep_page.ids.ml_ep
        # episode_page_button = main_widget.ids.ep_page.ids.btn_t
        # episode_page_button.text = 'heyboui'
        # episode_page_button.canvas.ask_update()
        # test = OneLineListItem(text="heyboiu")
        #
        # episode_page_list.add_widget(OneLineListItem(text='hello'))
        # Global.EP_PAGE_EPISODE = episode
        # Global.EP_PAGE_ANIME = anime_name
        # self.root.ids.ep_page.ids.btn_t.on_release()
        self.navigate('ep_page')

    def load_home(self,main_widget):
        home_anime_list = main_widget.ids.home.ids.ani_list
        db = TinyDB(Global.DB_FILE)
        anime_db = db.all()

        if len(home_anime_list.children) > 0:
            for anime in home_anime_list.children:
                print(anime.parent)


        for anime in anime_db:
            print('processing ' + anime["anime_name"])
            start_fetching_episodes_from =  0
            if anime["anime_name"] not in Global.ANIME_LIST:
                print('Gonna start then')
                anime_item = MDAccordionItem();
                anime_item.icon = 'movie'
                anime_item.title = anime["anime_name"]
                home_anime_list.add_widget(anime_item)
                if anime["episodes_out"] > 50:
                    start_fetching_episodes_from = anime["episodes_out"] - 50

                for episode in range(start_fetching_episodes_from, anime["episodes_out"]):
                    anime_sub_item = MDAccordionSubItem(parent_item = anime_item, text = 'Episode ' + str(episode + 1))
                    anime_sub_item.on_release = functools.partial(self.open_episode_page, episode + 1, anime["anime_name"], main_widget)
                    anime_item.add_widget(anime_sub_item)
                Global.ANIME_LIST.append(anime["anime_name"])

    def navigate(self, route):
        if route is 'home':
            self.load_home(self.root);
        self.root.ids.scr_mngr.current = route

    def build(self):
        kv_file = resource_path(os.path.join('templates', 'navigation.kv'))
        main_widget = Builder.load_file(kv_file)
        episode_page_class = episode_page.Episode_Page(name='ep_page')
        main_widget.ids.scr_mngr.add_widget(criterea_selection.Criterea_Selection(name='crits'))
        main_widget.ids.scr_mngr.add_widget(home.Home(name='home'))
        main_widget.ids.scr_mngr.add_widget(episode_page_class)
        Global.EPISODE_PAGE_CLASS = episode_page_class
        self.load_home(main_widget)
        return main_widget




if __name__ == '__main__':
    set_season()
    load_create_tinydb()
    WGTS().run()
