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


class Episode_Page(Screen):
    def search(self, anime_name, episode):
        print('Hey boi')
        self.ids.search_param.text = anime_name + ' episode ' + str(episode)
        self.ids.ml_ep.add_widget(OneLineListItem(text="HeyMan"))

    def go_back(self):
        self.manager.transition.direction = 'right'
        self.manager.current = 'home'
    pass
